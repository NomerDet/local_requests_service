from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    CHAR,
    SMALLINT,
    MEDIUMINT,
    DATE
)

from models.BaseModel import EntityMeta


class AutoSession(EntityMeta):
    __tablename__ = "auto_session_tbl"
    auto_request_id = Column("auto_request_id", MEDIUMINT, primary_key=True, autoincrement=True)
    userenter_id = Column("userenter_id", SMALLINT)
    userleave_id = Column("userleave_id", SMALLINT)
    post_enter_id = Column("post_enter_id", MEDIUMINT)
    dateenter_fld = Column("dateenter_fld", CHAR(20))
    dateleave_fld = Column("dateleave_fld", CHAR(20))
    post_leave_id = Column("post_leave_id", MEDIUMINT)
