from fastapi import APIRouter, Depends, Response, status

import simplejson as json
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services.AutoRequestService import AutoRequestService
from schemas.pydantic.AutoRequestSchema import AutoRequestSchema, AutoTbl, AutoRequestTbl
from schemas.pydantic.BlacklistSchema import BlacklistSchema, SecobjectsAutoBlacklistTbl
from schemas.pydantic.LimitsSchema import LimitsSchema, SecobjectsTenantTbl

AutoRequestRouter = APIRouter(prefix="/v1/auto_request", tags=["auto_request"])


@AutoRequestRouter.get(
    "/check/"
)
def check(
        response: Response,
        mode: str,
        auto_request_id: int,
        post_id: int,
        overlimit: int = 0,
        autoRequestService: AutoRequestService = Depends()):
    if mode == 'auto_request_enter':
        if autoRequestService.check_auto_request_enter(auto_request_id, post_id):
            response.status_code = 200
        else:
            response.status_code = 403

    else:
        if autoRequestService.check_auto_request_leave(auto_request_id, post_id, overlimit):
            response.status_code = 200
        else:
            response.status_code = 403
    return


@AutoRequestRouter.post(
    "/add/",
    status_code=status.HTTP_201_CREATED
)
def add(
        auto_request: AutoRequestSchema,
        autoRequestService: AutoRequestService = Depends()):

    print("TEST")
    data = json.loads(auto_request.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if auto_request.token == '2332fasdfsd1234123sd213e21':
        if isinstance(auto_request.auto_request_tbl, AutoRequestTbl) and \
                isinstance(auto_request.auto_request_tbl.auto_request_id, int):
            autoRequestService.add_auto_request(auto_request.auto_request_tbl,
                                                auto_request.auto_tbl,
                                                auto_request.auto_request_post_tbl,
                                                auto_request.auto_request_sched_tbl)
        else:
            print({'detail': 'check input data for ADD operation', 'data': data})
            return JSONResponse(
                content=jsonable_encoder({'detail': 'check input data for ADD operation', 'data': data}),
                status_code=status.HTTP_400_BAD_REQUEST
            )


@AutoRequestRouter.post(
    "/edit/",
    status_code=status.HTTP_201_CREATED
)
def edit(
        auto_request: AutoRequestSchema,
        autoRequestService: AutoRequestService = Depends()):

    data = json.loads(auto_request.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if auto_request.token == '2332fasdfsd1234123sd213e21':
        if isinstance(auto_request.auto_request_tbl, AutoRequestTbl) and \
                isinstance(auto_request.auto_request_tbl.auto_request_id, int):
            autoRequestService.edit_auto_request(auto_request.auto_request_tbl,
                                                auto_request.auto_tbl,
                                                auto_request.auto_request_post_tbl,
                                                auto_request.auto_request_sched_tbl)
        else:
            print({'detail': 'check input data for EDIT operation', 'data': data})

            return JSONResponse(
                content=jsonable_encoder({'detail': 'check input data for EDIT operation', 'data': data}),
                status_code=status.HTTP_400_BAD_REQUEST
            )


@AutoRequestRouter.post(
    "/delete/",
    status_code=status.HTTP_201_CREATED
)
def delete(
        auto_request: AutoRequestSchema,
        autoRequestService: AutoRequestService = Depends()):

    data = json.loads(auto_request.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if auto_request.token == '2332fasdfsd1234123sd213e21':
        if isinstance(auto_request.auto_request_tbl, AutoRequestTbl) and \
                isinstance(auto_request.auto_request_tbl.auto_request_id, int):
            autoRequestService.delete_auto_request(auto_request.auto_request_tbl)
        else:
            print({'detail': 'check input data for DELETE operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for DELETE operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)

@AutoRequestRouter.post(
    "/add_bl/",
    status_code=status.HTTP_201_CREATED
)
def add_bl(
        blacklist: BlacklistSchema,
        autoRequestService: AutoRequestService = Depends()):

    data = json.loads(blacklist.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if blacklist.token == '2332fasdfsd1234123sd213e21':
        if isinstance(blacklist.secobjects_auto_blacklist_tbl, SecobjectsAutoBlacklistTbl) and \
                isinstance(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id, int):
            autoRequestService.add_blacklist(blacklist.secobjects_auto_blacklist_tbl)
        else:
            print({'detail': 'check input data for ADD BL operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for ADD BL operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)

@AutoRequestRouter.post(
    "/del_bl/",
    status_code=status.HTTP_201_CREATED
)
def delete_bl(
        blacklist: BlacklistSchema,
        autoRequestService: AutoRequestService = Depends()):

    data = json.loads(blacklist.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if blacklist.token == '2332fasdfsd1234123sd213e21':
        if isinstance(blacklist.secobjects_auto_blacklist_tbl, SecobjectsAutoBlacklistTbl) and \
                isinstance(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id, int):
            autoRequestService.delete_blacklist(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id)
        else:
            print({'detail': 'check input data for DELETE BL operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for DELETE BL operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)


@AutoRequestRouter.post(
    "/add_limits/",
    status_code=status.HTTP_201_CREATED
)
def add_limits(
        secobjects_tenant: LimitsSchema,
        autoRequestService: AutoRequestService = Depends()):

    data = json.loads(secobjects_tenant.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if secobjects_tenant.token == '2332fasdfsd1234123sd213e21':
        if isinstance(secobjects_tenant.secobjects_tenant_tbl, SecobjectsTenantTbl):
            autoRequestService.add_limit(secobjects_tenant)
        else:
            print({'detail': 'check input data for ADD LIMIT operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for ADD LIMIT operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)

