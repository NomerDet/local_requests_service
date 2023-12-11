from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    CHAR,
    DATE,
    MEDIUMINT,
    VARCHAR,
    TEXT
)

from models.BaseModel import EntityMeta


class Auto(EntityMeta):
    __tablename__ = "auto_tbl"
    auto_id = Column("auto_id", MEDIUMINT, primary_key=True, autoincrement=True)
    autobrand_fld = Column("autobrand_fld", VARCHAR(30))
    number_fld = Column("number_fld", CHAR(15))

    modified_fld = Column("modified_fld", CHAR(20))
    acomment_fld = Column("acomment_fld", TEXT)
    created_fld = Column("created_fld", DATE)
    digits_fld = Column("digits_fld", CHAR(10))

    def normalize(self):
        return {
            "auto_id": self.auto_id.__int__(),
            "autobrand_fld": self.autobrand_fld.__str__(),
            "number_fld": self.number_fld.__str__(),

            "modified_fld": self.modified_fld.__str__(),
            "acomment_fld": self.acomment_fld.__str__(),
            "created_fld": self.created_fld.__str__(),
            "digits_fld": self.digits_fld.__str__(),
        }