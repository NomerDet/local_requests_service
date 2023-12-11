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


class AutoRequestSched(EntityMeta):
    __tablename__ = "auto_request_sched_tbl"
    auto_request_id = Column("auto_request_id", MEDIUMINT, primary_key=True, autoincrement=True)
    weekday_fld = Column("weekday_fld", TINYINT, primary_key=True)
    from_fld = Column("from_fld", TIME)
    to_fld = Column("to_fld", TIME)
    modified_fld = Column("modified_fld", CHAR(20))

    def normalize(self):
        return {
            "auto_request_id": self.auto_request_id.__int__() if self.auto_request_id is not None else None,
            "weekday_fld": self.weekday_fld.__int__() if self.weekday_fld is not None else None,
            "from_fld": self.from_fld.__str__() if self.from_fld is not None else None,
            "to_fld": self.to_fld.__str__() if self.to_fld is not None else None,
            "modified_fld": self.modified_fld.__str__() if self.modified_fld is not None else None,
        }
