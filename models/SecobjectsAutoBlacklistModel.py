from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    CHAR,
    MEDIUMINT,
    SMALLINT,
    VARCHAR
)

from models.BaseModel import EntityMeta


class SecobjectsAutoBlacklist(EntityMeta):
    __tablename__ = "secobjects_auto_blacklist_tbl"
    secobjects_auto_blacklist_id = Column("secobjects_auto_blacklist_id", MEDIUMINT, primary_key=True, autoincrement=True)
    number_fld = Column("number_fld", CHAR(15))
    secobjects_id = Column("secobjects_id", SMALLINT)
    comment_fld = Column("comment_fld", VARCHAR(255))
    autobrand_fld = Column("autobrand_fld", VARCHAR(30))