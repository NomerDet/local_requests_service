from sqlalchemy import Column,func
from sqlalchemy.dialects.mysql import (
    BOOLEAN,
    CHAR,
    DATETIME,
    MEDIUMINT,
)

from models.BaseModel import EntityMeta
import datetime


class AutoSpecLog(EntityMeta):
    __tablename__ = "auto_spec_log_tbl"
    id = Column("id", MEDIUMINT, primary_key=True, autoincrement=True)
    post_id = Column("post_id", MEDIUMINT)
    direction = Column("direction", CHAR(18))
    spec_class = Column("spec_class", CHAR(11))
    number = Column("number", CHAR(11))
    timestamp = Column("timestamp", CHAR(20))
    uploaded = Column("uploaded", BOOLEAN, default=False)
