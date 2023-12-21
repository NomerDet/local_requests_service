from pydantic import BaseModel
from typing import Dict, List, Optional, Tuple, Union
from typing import Optional, Type, Any, Tuple
from copy import deepcopy
from typing_extensions import Annotated

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from pydantic.functional_validators import AfterValidator


def is_null(v: Any) -> Any:
    # validation disabled
    # assert v is not None, f'Should not be None!'
    return v


class SecobjectsTenantTbl(BaseModel):
    secobjects_tenant_id:           Annotated[Optional[int], AfterValidator(is_null)] = None
    autorequest_perm_limit_fld:     Annotated[Optional[int], AfterValidator(is_null)] = None
    autorequest_temp_limit_fld:     Annotated[Optional[int], AfterValidator(is_null)] = None
    temp_limit_force_fld:           Annotated[Optional[int], AfterValidator(is_null)] = None
    perm_limit_force_fld:           Annotated[Optional[int], AfterValidator(is_null)] = None


class SecobjectsTenantSchema(BaseModel):
    secobjects_tenant_tbl: SecobjectsTenantTbl
    token: str
