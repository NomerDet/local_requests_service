from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    SMALLINT,
)

from models.BaseModel import EntityMeta


class User(EntityMeta):
    __tablename__ = "user_tbl"
    user_id = Column("user_id", SMALLINT, primary_key=True, autoincrement=True)
