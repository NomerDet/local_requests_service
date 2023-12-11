from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    CHAR,
    DATE,
    MEDIUMINT,
    SMALLINT,
    TEXT,
    TINYINT,
    TIME,
    TIMESTAMP,
    VARCHAR,
)

from models.BaseModel import EntityMeta


class AutoRequest(EntityMeta):
    __tablename__ = "auto_request_tbl"
    auto_id = Column("auto_id", MEDIUMINT)
    auto_request_id = Column("auto_request_id", MEDIUMINT, primary_key=True, autoincrement=True)
    comment_fld = Column("comment_fld", TEXT)
    created_fld = Column("created_fld", TIMESTAMP)

    date_fld = Column("date_fld", CHAR(20))
    dateenter_fld = Column("dateenter_fld", CHAR(20))
    datefrom_fld = Column("datefrom_fld", CHAR(20))
    dateleave_fld = Column("dateleave_fld", CHAR(20))

    dateto_fld = Column("dateto_fld", CHAR(20))
    modified_fld = Column("modified_fld", CHAR(20))
    permanent_fld = Column("permanent_fld", TINYINT)
    place_fld = Column("place_fld", VARCHAR(45))

    request_status_id = Column("request_status_id", TINYINT)
    sec_fld = Column("sec_fld", TINYINT)
    secobjects_id = Column("secobjects_id", SMALLINT)
    secobjects_post_id = Column("secobjects_post_id", SMALLINT)

    secobjects_tenant_id = Column("secobjects_tenant_id", MEDIUMINT)
    status_changed_fld = Column("status_changed_fld", CHAR(20))
    # time_fld = Column("time_fld", TIME)
    schedule_fld = Column("schedule_fld", TINYINT)
    usercreated_id = Column("usercreated_id", SMALLINT)

    userenter_id = Column("userenter_id", SMALLINT)
    userleave_id = Column("userleave_id", SMALLINT)
    usermodified_id = Column("usermodified_id", SMALLINT)
    userstatus_id = Column("userstatus_id", SMALLINT)
    vip_fld = Column("vip_fld", TINYINT)

    def normalize(self):
        return {
            "auto_id": self.auto_id.__int__() if self.auto_id is not None else None,
            "auto_request_id": self.auto_request_id.__int__() if self.auto_request_id is not None else None,
            "comment_fld": self.comment_fld.__str__() if self.comment_fld is not None else None,
            "created_fld": self.created_fld.__str__() if self.created_fld is not None else None,

            "date_fld": self.date_fld.__str__() if self.date_fld is not None else None,
            "dateenter_fld": self.dateenter_fld.__str__() if self.dateenter_fld is not None else None,
            "datefrom_fld": self.datefrom_fld.__str__() if self.datefrom_fld is not None else None,
            "dateleave_fld": self.dateleave_fld.__str__() if self.dateleave_fld is not None else None,

            "dateto_fld": self.dateto_fld.__str__() if self.dateto_fld is not None else None,
            "modified_fld": self.modified_fld.__str__() if self.modified_fld is not None else None,
            "permanent_fld": self.permanent_fld.__int__() if self.permanent_fld is not None else None,
            "place_fld": self.place_fld.__str__() if self.place_fld is not None else None,

            "request_status_id": self.request_status_id.__int__() if self.request_status_id is not None else None,
            "sec_fld": self.sec_fld.__int__() if self.sec_fld is not None else None,
            "secobjects_id": self.secobjects_id.__int__() if self.secobjects_id is not None else None,
            "secobjects_post_id": self.secobjects_post_id.__int__() if self.secobjects_post_id is not None else None,

            "secobjects_tenant_id": self.secobjects_tenant_id.__int__() if self.secobjects_tenant_id is not None else None,
            "status_changed_fld": self.status_changed_fld.__str__() if self.status_changed_fld is not None else None,
            # "time_fld": self.time_fld.__str__() if self.time_fld is not None else None,
            "schedule_fld": self.schedule_fld.__int__() if self.schedule_fld is not None else None,
            "usercreated_id": self.usercreated_id.__int__() if self.usercreated_id is not None else None,

            "userenter_id": self.userenter_id.__int__() if self.userenter_id is not None else None,
            "userleave_id": self.userleave_id.__int__() if self.userleave_id is not None else None,
            "usermodified_id": self.usermodified_id.__int__() if self.usermodified_id is not None else None,
            "userstatus_id": self.userstatus_id.__int__() if self.userstatus_id is not None else None,
            "vip_fld": self.vip_fld.__int__() if self.vip_fld is not None else None,
        }
