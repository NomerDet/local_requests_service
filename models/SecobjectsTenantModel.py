from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    MEDIUMINT,
    TINYINT,
    VARCHAR,
)

from models.BaseModel import EntityMeta


class SecobjectsTenant(EntityMeta):
    __tablename__ = "secobjects_tenant_tbl"
    secobjects_tenant_id = Column("secobjects_tenant_id", MEDIUMINT, primary_key=True, autoincrement=True)
    secobjects_tenant_fld = Column("secobjects_tenant_fld", VARCHAR(256))
    autorequest_perm_limit_fld = Column("autorequest_perm_limit_fld", TINYINT)
    autorequest_temp_limit_fld = Column("autorequest_temp_limit_fld", TINYINT)
    perm_limit_force_fld = Column("perm_limit_force_fld", TINYINT)
    temp_limit_force_fld = Column("temp_limit_force_fld", TINYINT)
