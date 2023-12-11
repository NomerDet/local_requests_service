import datetime
import time
from typing import Dict, List, Optional, Tuple, Union

from fastapi import Depends

from models.AutoRequestLogModel import AutoRequestLog
from models.AutoRequestModel import AutoRequest
from models.AutoRequestPostModel import AutoRequestPost
from models.AutoRequestSchedModel import AutoRequestSched
from models.AutoSessionModel import AutoSession
from models.AutoModel import Auto
from models.SecobjectsAutoBlacklistModel import SecobjectsAutoBlacklist
from models.SecobjectsTenantModel import SecobjectsTenant
from repositories.AutoRequestRepository import AutoRequestRepository
from schemas.pydantic.AutoRequestSchema import AutoRequestTbl, AutoTbl, AutoRequestPostTbl, AutoRequestSchedTbl
from schemas.pydantic.BlacklistSchema import BlacklistSchema, SecobjectsAutoBlacklistTbl
from schemas.pydantic.LimitsSchema import LimitsSchema, SecobjectsTenantTbl


class AutoRequestService:
    autoRequestRepository: AutoRequestRepository

    def __init__(self, autoRequestRepository: AutoRequestRepository = Depends()) -> None:
        self.autoRequestRepository = autoRequestRepository

    def check_auto_request_enter(self, req_id: int, post_id: int) -> bool:
        # Если статус - не "активна" - не пускать
        is_post = self.autoRequestRepository.get_post(req_id, post_id)
        auto_request_data = self.autoRequestRepository.get_auto_request_data(AutoRequest(auto_request_id=req_id))
        print(auto_request_data)
        if not auto_request_data:
            return False
        auto_request_data = auto_request_data.normalize()

        if not is_post and auto_request_data['request_status_id'] != 1:
            return False

        # Проверка по чёрному списку
        is_in_blacklist = self.autoRequestRepository.get_blacklist(auto_request_data['auto_id'],
                                                                   auto_request_data['secobjects_id'])
        if is_in_blacklist:
            return False

        if auto_request_data['schedule_fld']:
            auto_request_sched_data = self.autoRequestRepository.get_auto_request_sched(req_id)
            today_day_number = datetime.datetime.now().weekday() + 1
            for auto_request_sched in auto_request_sched_data:
                auto_request_sched_norm = auto_request_sched[0].normalize()

                if auto_request_sched_norm['weekday_fld'] == today_day_number:
                    if time.strptime(auto_request_sched_norm['from_fld'], '%H:%M:%S') <= time.strptime(datetime.datetime.now().strftime("%H:%M:%S"), '%H:%M:%S') <= time.strptime(auto_request_sched_norm['to_fld'], '%H:%M:%S'):
                        ## UPDATE TABLE LOG
                        self.autoRequestRepository.push_auto_request_log(
                            AutoRequestLog(
                                auto_request_id=req_id,
                                post_id=post_id,
                                direction='auto_request_enter',
                            )
                        )
                        return True
            return False


        limits_data = self.autoRequestRepository.get_limits(auto_request_data['secobjects_tenant_id'])

        limits = {}
        active = {}
        lim_force = {}
        tlimits = {}
        tactive = {}
        tlim_force = {}

        for limit_d in limits_data:
            if limit_d[0].permanent_fld:
                limits[auto_request_data['secobjects_tenant_id']] = limit_d[1].autorequest_perm_limit_fld
                active[auto_request_data['secobjects_tenant_id']] = limit_d[2]
                lim_force[auto_request_data['secobjects_tenant_id']] = limit_d[1].perm_limit_force_fld
            else:
                tlimits[auto_request_data['secobjects_tenant_id']] = limit_d[1].autorequest_temp_limit_fld
                tactive[auto_request_data['secobjects_tenant_id']] = limit_d[2]
                tlim_force[auto_request_data['secobjects_tenant_id']] = limit_d[1].temp_limit_force_fld

        # Исчерпан жесткий лимит постоянных заявок
        if auto_request_data['permanent_fld'] and \
                limits.get(auto_request_data['secobjects_tenant_id'], 0) and \
                (limits[auto_request_data['secobjects_tenant_id']] <= active[
                    auto_request_data['secobjects_tenant_id']]) and \
                lim_force[auto_request_data['secobjects_tenant_id']]:
            return False
        # Исчерпан обычный лимит постоянных заявок
        elif auto_request_data['permanent_fld'] and \
                limits.get(auto_request_data['secobjects_tenant_id'], 0) and \
                (limits[auto_request_data['secobjects_tenant_id']] <= active[
                    auto_request_data['secobjects_tenant_id']]) and \
                not lim_force[auto_request_data['secobjects_tenant_id']]:
            # Признак превышения лимита - создаём новую заявку и открываем
            # self.auto_request_enter(1, req_id, post_id)
            print('Признак превышения лимита - создаём новую заявку и открываем1')

            ## UPDATE TABLE LOG
            self.autoRequestRepository.push_auto_request_log(
                AutoRequestLog(
                    auto_request_id=req_id,
                    post_id=post_id,
                    direction='auto_request_enter',
                )
            )
            return True
        # Исчерпан жесткий лимит временных заявок
        elif not auto_request_data['permanent_fld'] and \
                tlimits.get(auto_request_data['secobjects_tenant_id'], 0) and \
                (tlimits[auto_request_data['secobjects_tenant_id']] <= tactive[
                    auto_request_data['secobjects_tenant_id']]) and \
                tlim_force[auto_request_data['secobjects_tenant_id']]:
            return False
        elif not auto_request_data['permanent_fld'] and \
                tlimits.get(auto_request_data['secobjects_tenant_id'], 0) and \
                (tlimits[auto_request_data['secobjects_tenant_id']] <= tactive[
                    auto_request_data['secobjects_tenant_id']]) and \
                not tlim_force[auto_request_data['secobjects_tenant_id']]:
            # Признак превышения лимита - создаём новую заявку и открываем
            print('Признак превышения лимита - создаём новую заявку и открываем2')
            # self.auto_request_enter(1, req_id, post_id)

            ## UPDATE TABLE LOG
            self.autoRequestRepository.push_auto_request_log(
                AutoRequestLog(
                    auto_request_id=req_id,
                    post_id=post_id,
                    direction='auto_request_enter',
                )
            )
            return True

        else:
            # Нет лимитов - запускаем
            # Проверка, нужно ли открывать заявку
            if auto_request_data["dateenter_fld"] == '0000-00-00 00:00:00' or \
                    auto_request_data["dateleave_fld"] != '0000-00-00 00:00:00':
                self.auto_request_enter(0, req_id, post_id)

                ## UPDATE TABLE LOG
                self.autoRequestRepository.push_auto_request_log(
                    AutoRequestLog(
                        auto_request_id=req_id,
                        post_id=post_id,
                        direction='auto_request_enter',
                    )
                )
                return True
            # Просто отдаём 200
            else:
                ## UPDATE TABLE LOG
                self.autoRequestRepository.push_auto_request_log(
                    AutoRequestLog(
                        auto_request_id=req_id,
                        post_id=post_id,
                        direction='auto_request_enter',
                    )
                )
                return True

    def check_auto_request_leave(self, req_id: int, post_id: int, overlimit: int) -> bool:
        is_post = self.autoRequestRepository.get_post(req_id, post_id)
        if not is_post and not post_id:
            return False

        if req_id:
            self.auto_request_leave(req_id, post_id)

        self.autoRequestRepository.push_auto_request_log(
            AutoRequestLog(
                auto_request_id=req_id,
                post_id=post_id,
                direction='auto_request_leave',
                overlimit=True if overlimit else False,
            )
        )
        return True

    def auto_request_enter(self, overlimit: int, req_id: int, post_id: int):
        auto_request_id = req_id
        # if overlimit:
        #     auto_request_id = self.autoRequestRepository.create_auto_request_enter_overlimit(auto_request_id)
        #     self.autoRequestRepository.add_post_auto_request_enter(req_id, auto_request_id)
        opened = self.autoRequestRepository.is_session_opened(auto_request_id)

        if opened:
            max_ = self.autoRequestRepository.is_session_opened_earlier(auto_request_id)

            if max_ != opened:
                self.autoRequestRepository.close_earlier_sessions(auto_request_id)
            else:
                return

        self.autoRequestRepository.update_auto_request_enter(auto_request_id)
        # TODO случаются ошибки, связанные с тем, что ключ сессии уже сущесвтует. проверить ветку условий выше
        self.autoRequestRepository.add_enter_to_sessions(
            AutoSession(
                auto_request_id=auto_request_id,
                userenter_id=1,
                dateenter_fld=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                dateleave_fld='0000-00-00 00:00:00',
                post_enter_id=post_id
            )
        )

    def auto_request_leave(self, req_id: int, post_id: int):
        self.autoRequestRepository.update_auto_request_leave(req_id)
        self.autoRequestRepository.update_leave_in_sessions(req_id, post_id)

    def add_auto_request(self,
                         auto_request_tbl: AutoRequestTbl,
                         auto_tbl: Optional[AutoTbl],
                         auto_request_post_tbls: List[AutoRequestPostTbl],
                         auto_request_sched_tbls: Optional[List[AutoRequestSchedTbl]]):
        self.autoRequestRepository.add_auto_request(
            AutoRequest(
                auto_id=auto_request_tbl.auto_id,
                auto_request_id=auto_request_tbl.auto_request_id,
                comment_fld=auto_request_tbl.comment_fld,
                created_fld=auto_request_tbl.created_fld,
                date_fld=auto_request_tbl.date_fld,
                dateenter_fld=auto_request_tbl.dateenter_fld,
                datefrom_fld=auto_request_tbl.datefrom_fld,
                dateleave_fld=auto_request_tbl.dateleave_fld,
                dateto_fld=auto_request_tbl.dateto_fld,
                modified_fld=auto_request_tbl.modified_fld,
                permanent_fld=auto_request_tbl.permanent_fld,
                place_fld=auto_request_tbl.place_fld,
                request_status_id=auto_request_tbl.request_status_id,
                sec_fld=auto_request_tbl.sec_fld,
                secobjects_id=auto_request_tbl.secobjects_id,
                secobjects_post_id=auto_request_tbl.secobjects_post_id,
                secobjects_tenant_id=auto_request_tbl.secobjects_tenant_id,
                status_changed_fld=auto_request_tbl.status_changed_fld,
                # time_fld=auto_request_tbl.time_fld,
                schedule_fld=auto_request_tbl.schedule_fld,
                usercreated_id=auto_request_tbl.usercreated_id,
                userenter_id=auto_request_tbl.userenter_id,
                userleave_id=auto_request_tbl.userleave_id,
                usermodified_id=auto_request_tbl.usermodified_id,
                userstatus_id=auto_request_tbl.userstatus_id,
                vip_fld=auto_request_tbl.vip_fld
            )
        )
        for auto_request_post_tbl in auto_request_post_tbls:
            self.autoRequestRepository.add_auto_request_post(
                AutoRequestPost(
                    auto_request_id=auto_request_post_tbl.auto_request_id,
                    secobjects_post_id=auto_request_post_tbl.secobjects_post_id,
                )
            )
        if isinstance(auto_tbl, AutoTbl) and isinstance(auto_tbl.auto_id, int):
            self.autoRequestRepository.add_auto(
                Auto(
                    auto_id=auto_tbl.auto_id,
                    autobrand_fld=auto_tbl.autobrand_fld,
                    number_fld=auto_tbl.number_fld,
                    modified_fld=auto_tbl.modified_fld,
                    acomment_fld=auto_tbl.acomment_fld,
                    created_fld=auto_tbl.created_fld,
                    digits_fld=auto_tbl.digits_fld,
                )
            )
        if isinstance(auto_request_sched_tbls, List):
            for auto_request_sched_tbl in auto_request_sched_tbls:
                self.autoRequestRepository.add_auto_request_sched(
                    AutoRequestSched(
                        auto_request_id=auto_request_sched_tbl.auto_request_id,
                        from_fld=auto_request_sched_tbl.from_fld,
                        to_fld=auto_request_sched_tbl.to_fld,
                        weekday_fld=auto_request_sched_tbl.weekday_fld,
                    )
                )

    def edit_auto_request(self,
                         auto_request_tbl: AutoRequestTbl,
                         auto_tbl: Optional[AutoTbl],
                         auto_request_post_tbls: List[AutoRequestPostTbl],
                         auto_request_sched_tbls: Optional[List[AutoRequestSchedTbl]]):
        if isinstance(auto_request_tbl, AutoRequestTbl):
            self.autoRequestRepository.edit_auto_request(
                AutoRequest(
                    auto_id=auto_request_tbl.auto_id,
                    auto_request_id=auto_request_tbl.auto_request_id,
                    comment_fld=auto_request_tbl.comment_fld,
                    created_fld=auto_request_tbl.created_fld,
                    date_fld=auto_request_tbl.date_fld,
                    dateenter_fld=auto_request_tbl.dateenter_fld,
                    datefrom_fld=auto_request_tbl.datefrom_fld,
                    dateleave_fld=auto_request_tbl.dateleave_fld,
                    dateto_fld=auto_request_tbl.dateto_fld,
                    modified_fld=auto_request_tbl.modified_fld,
                    permanent_fld=auto_request_tbl.permanent_fld,
                    place_fld=auto_request_tbl.place_fld,
                    request_status_id=auto_request_tbl.request_status_id,
                    sec_fld=auto_request_tbl.sec_fld,
                    secobjects_id=auto_request_tbl.secobjects_id,
                    secobjects_post_id=auto_request_tbl.secobjects_post_id,
                    secobjects_tenant_id=auto_request_tbl.secobjects_tenant_id,
                    status_changed_fld=auto_request_tbl.status_changed_fld,
                    # time_fld=auto_request_tbl.time_fld,
                    schedule_fld=auto_request_tbl.schedule_fld,
                    usercreated_id=auto_request_tbl.usercreated_id,
                    userenter_id=auto_request_tbl.userenter_id,
                    userleave_id=auto_request_tbl.userleave_id,
                    usermodified_id=auto_request_tbl.usermodified_id,
                    userstatus_id=auto_request_tbl.userstatus_id,
                    vip_fld=auto_request_tbl.vip_fld
                )
            )
        if isinstance(auto_tbl, AutoTbl):
            self.autoRequestRepository.edit_auto(
                Auto(
                    auto_id=auto_tbl.auto_id,
                    autobrand_fld=auto_tbl.autobrand_fld,
                    number_fld=auto_tbl.number_fld,
                    modified_fld=auto_tbl.modified_fld,
                    acomment_fld=auto_tbl.acomment_fld,
                    created_fld=auto_tbl.created_fld,
                    digits_fld=auto_tbl.digits_fld,
                )
            )
        if isinstance(auto_request_post_tbls, List):
            for auto_request_post_tbl in auto_request_post_tbls:
                self.autoRequestRepository.edit_auto_request_post(
                    AutoRequestPost(
                        auto_request_id=auto_request_post_tbl.auto_request_id,
                        secobjects_post_id=auto_request_post_tbl.secobjects_post_id,
                    )
                )
        if isinstance(auto_request_sched_tbls, List):
            for auto_request_sched_tbl in auto_request_sched_tbls:
                # self.autoRequestRepository.edit_auto_request_sched({k: v for k, v in auto_request_sched_tbl.model_dump().items() if v})
                self.autoRequestRepository.edit_auto_request_sched(
                    AutoRequestSched(
                        auto_request_id=auto_request_sched_tbl.auto_request_id,
                        from_fld=auto_request_sched_tbl.from_fld,
                        to_fld=auto_request_sched_tbl.to_fld,
                        weekday_fld=auto_request_sched_tbl.weekday_fld,
                    )
                )

    def delete_auto_request(self, auto_request_tbl: AutoRequestTbl):
        self.autoRequestRepository.delete_auto_request(auto_request_tbl.auto_request_id)

    def add_blacklist(self, secobjects_auto_blacklist_tbl: SecobjectsAutoBlacklistTbl):
        self.autoRequestRepository.add_blacklist(
            SecobjectsAutoBlacklist(
                secobjects_auto_blacklist_id=secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id,
                number_fld=secobjects_auto_blacklist_tbl.number_fld,
                secobjects_id=secobjects_auto_blacklist_tbl.secobjects_id,
                autobrand_fld=secobjects_auto_blacklist_tbl.autobrand_fld,
                comment_fld=secobjects_auto_blacklist_tbl.comment_fld
            )
        )

    def delete_blacklist(self, secobjects_auto_blacklist_id: int):
        self.autoRequestRepository.delete_blacklist(secobjects_auto_blacklist_id)

    def add_limit(self, secobjects_tenant_tbl: SecobjectsTenantTbl):
        self.autoRequestRepository.add_limit(
            SecobjectsTenant(
                autorequest_perm_limit_fld=secobjects_tenant_tbl.autorequest_perm_limit_fld,
                autorequest_temp_limit_fld=secobjects_tenant_tbl.autorequest_temp_limit_fld,
                perm_limit_force_fld=secobjects_tenant_tbl.perm_limit_force_fld,
                temp_limit_force_fld=secobjects_tenant_tbl.temp_limit_force_fld
            )
        )