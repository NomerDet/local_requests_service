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


class SecobjectsAutoBlacklistTbl(BaseModel):
    secobjects_auto_blacklist_id:   Annotated[Optional[int], AfterValidator(is_null)] = None
    comment_fld:                    Annotated[Optional[str], AfterValidator(is_null)] = None
    autobrand_fld:                  Annotated[Optional[str], AfterValidator(is_null)] = None
    number_fld:                     Annotated[Optional[str], AfterValidator(is_null)] = None
    secobjects_id:                  Annotated[Optional[str], AfterValidator(is_null)] = None


class BlacklistSchema(BaseModel):
    secobjects_auto_blacklist_tbl: SecobjectsAutoBlacklistTbl
    token: str
