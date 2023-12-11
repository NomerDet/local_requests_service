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


class AutoRequestTbl(BaseModel):
    # https://docs.pydantic.dev/latest/concepts/validators/
    # https://github.com/pydantic/pydantic/issues/1223
    auto_id:                Annotated[Optional[int], AfterValidator(is_null)] = None
    auto_request_id:        Annotated[Optional[int], AfterValidator(is_null)] = None
    comment_fld:            Annotated[Optional[str], AfterValidator(is_null)] = None
    created_fld:            Annotated[Optional[str], AfterValidator(is_null)] = None
    date_fld:               Annotated[Optional[str], AfterValidator(is_null)] = None
    dateenter_fld:          Annotated[Optional[str], AfterValidator(is_null)] = None
    datefrom_fld:           Annotated[Optional[str], AfterValidator(is_null)] = None
    dateleave_fld:          Annotated[Optional[str], AfterValidator(is_null)] = None
    dateto_fld:             Annotated[Optional[str], AfterValidator(is_null)] = None
    modified_fld:           Annotated[Optional[str], AfterValidator(is_null)] = None
    permanent_fld:          Annotated[Optional[int], AfterValidator(is_null)] = None
    place_fld:              Annotated[Optional[str], AfterValidator(is_null)] = None
    request_status_id:      Annotated[Optional[int], AfterValidator(is_null)] = None
    sec_fld:                Annotated[Optional[int], AfterValidator(is_null)] = None
    secobjects_id:          Annotated[Optional[int], AfterValidator(is_null)] = None
    secobjects_post_id:     Optional[int] = None
    secobjects_tenant_id:   Optional[int] = None
    status_changed_fld:     Optional[str] = None
    # time_fld:               Annotated[Optional[str], AfterValidator(is_null)] = None
    schedule_fld:           Annotated[Optional[int], AfterValidator(is_null)] = None
    usercreated_id:         Annotated[Optional[int], AfterValidator(is_null)] = None
    userenter_id:           Annotated[Optional[int], AfterValidator(is_null)] = None
    userleave_id:           Annotated[Optional[int], AfterValidator(is_null)] = None
    usermodified_id:        Annotated[Optional[int], AfterValidator(is_null)] = None
    userstatus_id:          Annotated[Optional[int], AfterValidator(is_null)] = None
    vip_fld:                Annotated[Optional[int], AfterValidator(is_null)] = None


class AutoRequestPostTbl(BaseModel):
    # https://docs.pydantic.dev/latest/concepts/validators/
    # https://github.com/pydantic/pydantic/issues/1223
    auto_request_id:        Annotated[Optional[int], AfterValidator(is_null)] = None
    secobjects_post_id:     Optional[int] = None


class AutoRequestSchedTbl(BaseModel):
    # https://docs.pydantic.dev/latest/concepts/validators/
    # https://github.com/pydantic/pydantic/issues/1223

    from_fld:           Annotated[Optional[str], AfterValidator(is_null)] = None
    to_fld:             Annotated[Optional[str], AfterValidator(is_null)] = None
    auto_request_id:    Annotated[Optional[int], AfterValidator(is_null)] = None
    weekday_fld:        Annotated[Optional[int], AfterValidator(is_null)] = None


class AutoTbl(BaseModel):
    modified_fld:   Annotated[Optional[str], AfterValidator(is_null)] = None
    autobrand_fld:  Annotated[Optional[str], AfterValidator(is_null)] = None
    number_fld:     Annotated[Optional[str], AfterValidator(is_null)] = None
    acomment_fld:   Annotated[Optional[str], AfterValidator(is_null)] = None
    created_fld:    Annotated[Optional[str], AfterValidator(is_null)] = None
    auto_id:        Annotated[Optional[int], AfterValidator(is_null)] = None
    digits_fld:     Annotated[Optional[int], AfterValidator(is_null)] = None


class AutoRequestSchema(BaseModel):
    auto_request_tbl: AutoRequestTbl
    token: str
    auto_tbl: Optional[AutoTbl] = None
    auto_request_post_tbl: List[AutoRequestPostTbl]
    auto_request_sched_tbl: Optional[List[AutoRequestSchedTbl]] = None
