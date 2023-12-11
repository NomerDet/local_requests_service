from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    MEDIUMINT,
)

from models.BaseModel import EntityMeta


class AutoRequestPost(EntityMeta):
    __tablename__ = "auto_request_post_tbl"
    auto_request_id = Column("auto_request_id", MEDIUMINT, primary_key=True, autoincrement=True)
    secobjects_post_id = Column("secobjects_post_id", MEDIUMINT, primary_key=True)
