from sqlalchemy import Column,func
from sqlalchemy.dialects.mysql import (
    BOOLEAN,
    CHAR,
    DATETIME,
    MEDIUMINT,
)

from models.BaseModel import EntityMeta
import datetime


class AutoRequestLog(EntityMeta):
    __tablename__ = "auto_request_log_tbl"
    id = Column("id", MEDIUMINT, primary_key=True, autoincrement=True)
    auto_request_id = Column("auto_request_id", MEDIUMINT)
    post_id = Column("post_id", MEDIUMINT)
    direction = Column("direction", CHAR(18))
    timestamp = Column("timestamp", DATETIME, default=func.now())
    uploaded = Column("uploaded", BOOLEAN, default=False)
    overlimit_enter = Column("overlimit_enter", BOOLEAN, default=False)
    overlimit_leave = Column("overlimit_leave", BOOLEAN, default=False)
