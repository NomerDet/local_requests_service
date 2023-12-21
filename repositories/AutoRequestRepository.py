from typing import List, Optional, Tuple
from datetime import datetime

from fastapi import Depends
from sqlalchemy import func, select, and_, cast, or_, insert, update, text, delete
from sqlalchemy.dialects.mysql import (
    CHAR,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import exists

from config.Database import (
    get_db_connection,
)
from models.AutoModel import Auto
from models.AutoRequestLogModel import AutoRequestLog
from models.AutoRequestModel import AutoRequest
from models.AutoRequestPostModel import AutoRequestPost
from models.AutoRequestSchedModel import AutoRequestSched
from models.AutoSessionModel import AutoSession
from models.SecobjectsAutoBlacklistModel import SecobjectsAutoBlacklist
from models.SecobjectsTenantModel import SecobjectsTenant

import uuid

class AutoRequestRepository:
    db: Session

    def __init__(
            self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def get_post(
            self,
            req_id: int,
            post_id: int,
    ) -> bool:
        stmt = exists(select(AutoRequestPost).where(
            and_(AutoRequestPost.auto_request_id == req_id, AutoRequestPost.secobjects_post_id == post_id))
        ).select()
        return self.db.execute(stmt).fetchall()[0][0]

    def get_auto_request_data(self, auto_request: AutoRequest) -> AutoRequest:
        return self.db.get(AutoRequest, auto_request.auto_request_id)

    def get_blacklist(
            self,
            auto_id: int,
            secobjects_id: int,
    ) -> bool:
        stmt = exists(
            select(SecobjectsAutoBlacklist).join(
                Auto, SecobjectsAutoBlacklist.number_fld == Auto.number_fld
            ).where(
                and_(
                    Auto.auto_id == auto_id,
                    SecobjectsAutoBlacklist.number_fld == Auto.number_fld,
                    SecobjectsAutoBlacklist.secobjects_id == secobjects_id
                )
            )
        ).select()
        return self.db.execute(stmt).fetchall()[0][0]

    def get_auto_request_sched(self, auto_request_id: int) -> List[AutoRequestSched]:
        stmt = select(AutoRequestSched).filter(AutoRequestSched.auto_request_id == auto_request_id)
        auto_request_sched_all = self.db.execute(stmt).fetchall()
        print("        print(auto_request_sched_all)")
        print(auto_request_sched_all)
        return auto_request_sched_all

    def get_limits(self, tenant_id: int) -> List[Tuple[Optional[AutoRequest], Optional[SecobjectsTenant], Optional[int]]]:
        stmt = select(
            AutoRequest,
            SecobjectsTenant,
            func.count()
        ).join(
            AutoSession,
            AutoRequest.auto_request_id == AutoSession.auto_request_id
        ).join(
            SecobjectsTenant,
            AutoRequest.secobjects_tenant_id == SecobjectsTenant.secobjects_tenant_id
        ).where(
            and_(
                cast(AutoSession.dateleave_fld, CHAR(20)) == "0000-00-00 00:00:00",
                AutoRequest.request_status_id == 1,
                SecobjectsTenant.secobjects_tenant_id == tenant_id,
                or_(
                    SecobjectsTenant.autorequest_perm_limit_fld > 0,
                    SecobjectsTenant.autorequest_temp_limit_fld > 0
                )
            )
        ).group_by(
            SecobjectsTenant.secobjects_tenant_id,
            AutoRequest.permanent_fld
        )

        return self.db.execute(stmt).fetchall()

    def push_auto_request_log(self, auto_request_log: AutoRequestLog):
        self.db.add(auto_request_log)
        self.db.commit()

    # def create_auto_request_enter_overlimit(self, auto_request_id: int) -> int:
    #     select_stmt = select(
    #         AutoRequest.auto_id,
    #         0,
    #         func.current_date(),
    #         AutoRequest.secobjects_id,
    #         AutoRequest.secobjects_post_id,
    #         AutoRequest.secobjects_tenant_id,
    #         AutoRequest.usercreated_id,
    #         # AutoRequest.place_fld,
    #         text("\"uuid_data :uuid_text\"").bindparams(uuid_text=str(uuid.uuid4())),
    #         text("\"Создана автоматичестки как копия :auto_request_id\"").bindparams(auto_request_id=auto_request_id),
    #         1
    #     ).where(AutoRequest.auto_request_id == auto_request_id)
    #
    #     insert_stmt = insert(AutoRequest).from_select(
    #         [
    #             "auto_id",
    #             "permanent_fld",
    #             "date_fld",
    #             "secobjects_id",
    #             "secobjects_post_id",
    #             "secobjects_tenant_id",
    #             "usercreated_id",
    #             "place_fld",
    #             "comment_fld",
    #             "request_status_id"
    #         ],
    #         select_stmt
    #     )
    #
    #     self.db.execute(insert_stmt)
    #     last_inserted_id = self.db.execute(text('SELECT LAST_INSERT_ID() AS id')).fetchone()[0]
    #     self.db.commit()
    #
    #     return last_inserted_id

    # def add_post_auto_request_enter(self, old_auto_request_id: int, new_auto_request_id: int):
    #     select_stmt = select(
    #         new_auto_request_id,
    #         AutoRequestPost.secobjects_post_id
    #     ).where(AutoRequestPost.auto_request_id == old_auto_request_id)
    #     insert_stmt = insert(AutoRequestPost).from_select(
    #         [
    #             "auto_request_id",
    #             "secobjects_post_id"
    #         ],
    #         select_stmt
    #     )
    #
    #     self.db.execute(insert_stmt)
    #     self.db.commit()

    def is_session_opened(self, auto_request_id: int) -> datetime:
        select_stmt = select(
            func.str_to_date(AutoSession.dateenter_fld, "%Y-%m-%d %H:%M:%S")
        ).where(
            and_(
                AutoSession.auto_request_id == auto_request_id,
                AutoSession.dateleave_fld == '0000-00-00 00:00:00'
            )
        )

        fetched_one = self.db.execute(select_stmt).fetchone()

        if not fetched_one:
            return None
        return fetched_one[0]

    def is_session_opened_earlier(self, auto_request_id: int) -> datetime:
        select_stmt = select(
            func.max(
                func.str_to_date(AutoSession.dateenter_fld, "%Y-%m-%d %H:%M:%S")
            )
        ).where(
            AutoSession.auto_request_id == auto_request_id
        )

        fetched_one = self.db.execute(select_stmt).fetchone()

        if not fetched_one:
            return None
        return fetched_one[0]

    def close_earlier_sessions(self, auto_request_id: int):
        update_stmt = update(AutoSession).values(
            dateleave_fld=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ).where(
            AutoSession.auto_request_id == auto_request_id
        )

        self.db.execute(update_stmt)
        self.db.commit()

    def update_auto_request_enter(self, auto_request_id: int):
        update_stmt = update(AutoRequest).values(
            dateenter_fld=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dateleave_fld='0000-00-00 00:00:00',
            userenter_id=1,
            userleave_id=None,
        ).where(
            AutoRequest.auto_request_id == auto_request_id
        )

        self.db.execute(update_stmt)
        self.db.commit()

    def add_enter_to_sessions(self, auto_session: AutoSession):
        self.db.add(auto_session)
        self.db.commit()

    def update_auto_request_leave(self, auto_request_id: int):
        update_stmt = update(AutoRequest).values(
            dateleave_fld=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            userleave_id=None
        ).where(
            AutoRequest.auto_request_id == auto_request_id
        )

        self.db.execute(update_stmt)
        self.db.commit()

    def update_leave_in_sessions(self, auto_request_id: int, post_id: int):
        select_stmt = select(AutoSession).where(
            AutoSession.auto_request_id == auto_request_id
        ).order_by(
            func.str_to_date(AutoSession.dateenter_fld, "%Y-%m-%d %H:%M:%S").desc()
        ).limit(1)

        fetched_one = self.db.execute(select_stmt).fetchone()

        if not fetched_one:
            return
        else:
            fetched_one_res = fetched_one[0]

        update_stmt = update(AutoSession).values(
            dateleave_fld=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            userleave_id=1,
            post_leave_id=post_id,
        ).where(
            and_(
                AutoSession.auto_request_id == auto_request_id,
                AutoSession.dateenter_fld == fetched_one_res.dateenter_fld
            )
        )

        self.db.execute(update_stmt)
        self.db.commit()

    def add_auto_request(self, auto_request: AutoRequest):
        auto_request_one = self.db.query(AutoRequest).filter(AutoRequest.auto_request_id == auto_request.auto_request_id)
        exist_auto_request = auto_request_one.first()
        if not exist_auto_request:
            self.db.add(auto_request)
            self.db.commit()

    def add_auto(self, auto: Auto):
        auto_one = self.db.query(Auto).filter(Auto.auto_id == auto.auto_id)
        exist_auto = auto_one.first()
        if not exist_auto:
            self.db.add(auto)
            self.db.commit()

    def add_auto_request_post(self, auto_request_post: AutoRequestPost):
        auto_request_post_one = self.db.query(AutoRequestPost).filter(and_(AutoRequestPost.auto_request_id == auto_request_post.auto_request_id, AutoRequestPost.secobjects_post_id == auto_request_post.secobjects_post_id))
        exist_auto_request_post = auto_request_post_one.first()
        if not exist_auto_request_post:
            self.db.add(auto_request_post)
            self.db.commit()

    def add_auto_request_sched(self, auto_request_sched: AutoRequestSched):
        auto_request_sched_one = self.db.query(AutoRequestSched).filter(and_(AutoRequestSched.auto_request_id == auto_request_sched.auto_request_id, AutoRequestSched.weekday_fld == auto_request_sched.weekday_fld))
        exist_auto_request_sched = auto_request_sched_one.first()
        if not exist_auto_request_sched:
            self.db.add(auto_request_sched)
            self.db.commit()

    def edit_auto_request(self, auto_request: AutoRequest):
        delete_stmt = delete(AutoRequest).where(AutoRequest.auto_request_id == auto_request.auto_request_id)
        # update_stmt = update(AutoRequest).values(**auto_request).where(AutoRequest.auto_request_id == auto_request['auto_request_id'])
        self.db.execute(delete_stmt)
        self.add_auto_request(auto_request)

    def edit_auto(self, auto: Auto):
        delete_stmt = delete(Auto).where(Auto.auto_id == auto.auto_id)
        # update_stmt = update(Auto).values(**auto).where(Auto.auto_id == auto['auto_id'])
        self.db.execute(delete_stmt)
        self.add_auto(auto)

    def edit_auto_request_post(self, auto_request_post: AutoRequestPost):
        delete_stmt = delete(AutoRequestPost).where(and_(AutoRequestPost.auto_request_id == auto_request_post.auto_request_id, AutoRequestPost.secobjects_post_id == auto_request_post.secobjects_post_id))
        # update_stmt = update(AutoRequest).values(**auto_request).where(AutoRequest.auto_request_id == auto_request['auto_request_id'])
        self.db.execute(delete_stmt)
        self.add_auto_request_post(auto_request_post)

    def edit_auto_request_sched(self, auto_request_sched: AutoRequestSched):
        delete_stmt = delete(AutoRequestSched).where(and_(AutoRequestSched.auto_request_id == auto_request_sched.auto_request_id, AutoRequestSched.weekday_fld == auto_request_sched.weekday_fld))
        # update_stmt = update(AutoRequest).values(**auto_request).where(AutoRequest.auto_request_id == auto_request['auto_request_id'])
        self.db.execute(delete_stmt)
        self.add_auto_request_sched(auto_request_sched)

    def delete_auto_request(self, auto_request_id: int):
        delete_stmt = delete(AutoRequest).where(AutoRequest.auto_request_id == auto_request_id)
        self.db.execute(delete_stmt)
        self.db.commit()

        delete_stmt = delete(AutoRequestSched).where(and_(AutoRequestSched.auto_request_id == auto_request_id))
        self.db.execute(delete_stmt)
        self.db.commit()

        delete_stmt = delete(AutoRequestPost).where(and_(AutoRequestPost.auto_request_id == auto_request_id))
        self.db.execute(delete_stmt)
        self.db.commit()

    def add_blacklist(self, blacklist: SecobjectsAutoBlacklist):
        blacklist_one = self.db.query(SecobjectsAutoBlacklist).filter(SecobjectsAutoBlacklist.secobjects_auto_blacklist_id == blacklist.secobjects_auto_blacklist_id)
        exist_blacklist = blacklist_one.first()
        if not exist_blacklist:
            self.db.add(blacklist)
            self.db.commit()

    def delete_blacklist(self, secobjects_auto_blacklist_id: int):
        delete_stmt = delete(SecobjectsAutoBlacklist).where(SecobjectsAutoBlacklist.secobjects_auto_blacklist_id == secobjects_auto_blacklist_id)
        self.db.execute(delete_stmt)
        self.db.commit()

    def add_client(self, limit: SecobjectsTenant):
        self.db.add(limit)
        self.db.commit()

    def edit_client(self, limit: dict):
        update_stmt = update(SecobjectsTenant).values(**limit).where(SecobjectsTenant.secobjects_tenant_id == limit['secobjects_tenant_id'])
        self.db.execute(update_stmt)
        self.db.commit()

    def del_client(self, secobjects_tenant_id: int):
        delete_auto_request_stmt = delete(AutoRequest).where(AutoRequest.secobjects_tenant_id == secobjects_tenant_id)
        delete_secobjects_tenant_stmt = delete(SecobjectsTenant).where(SecobjectsTenant.secobjects_tenant_id == secobjects_tenant_id)

        self.db.execute(delete_auto_request_stmt)
        self.db.execute(delete_secobjects_tenant_stmt)

        self.db.commit()

