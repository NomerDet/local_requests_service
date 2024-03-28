from fastapi import APIRouter, Depends, Response, status

import simplejson as json
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services.AutoRequestService import AutoRequestService
from schemas.pydantic.AutoRequestSchema import AutoRequestSchema, AutoTbl, AutoRequestTbl
from schemas.pydantic.BlacklistSchema import BlacklistSchema, SecobjectsAutoBlacklistTbl
from schemas.pydantic.SecobjectsTenantSchema import SecobjectsTenantSchema, SecobjectsTenantTbl

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
    """ Функция выполняет обработку GET запроса, эмулируя работу сайта для локальной проверки заявки

    :param response: Response
    :param mode: str - въезд или выезд
    :param auto_request_id: int - номер заявки
    :param post_id: int - номер шлагбаума
    :param overlimit: int - проезд по свехлимиту
    :param autoRequestService: AutoRequestService
    :return: None
    """
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

@AutoRequestRouter.get(
    "/spec/"
)
def spec(
        response: Response,
        mode: str,
        type: str,
        number: str,
        post_id: int,
        timestamp: str,
        autoRequestService: AutoRequestService = Depends()):
    """ Функция выполняет обработку GET запроса, эмулируя работу сайта для отложенной фиксации проезда спецтранспорта

    :param response: Response
    :param mode: str - въезд или выезд
    :param type: str - тип спецтранспорта (ambulance/firefighter/police)
    :param post_id: int - номер шлагбаума
    :param timestamp: str - временная метка вида "0000-00-00 00:00:00"
    :param autoRequestService: AutoRequestService
    :return: None
    """
    autoRequestService.set_spec_transit(mode, type, number, post_id, timestamp)
    response.status_code = 200

@AutoRequestRouter.post(
    "/add/",
    status_code=status.HTTP_201_CREATED
)
def add(
        auto_request: AutoRequestSchema,
        autoRequestService: AutoRequestService = Depends()):
    """ Функция выполняет добавление заявки на проезд авто в ЛокалБД от сайта

    :param auto_request: AutoRequestSchema
    :param autoRequestService: AutoRequestService
    :return: None
    """

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
            return
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
    """ Функция выполняет редактирование заявки на проезд авто в ЛокалБД от сайта

    :param auto_request: AutoRequestSchema
    :param autoRequestService: AutoRequestService
    :return: JSONResponse
    """

    data = json.loads(auto_request.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if auto_request.token == '2332fasdfsd1234123sd213e21':
        if isinstance(auto_request.auto_request_tbl, AutoRequestTbl) and \
                isinstance(auto_request.auto_request_tbl.auto_request_id, int):
            autoRequestService.edit_auto_request(auto_request.auto_request_tbl,
                                                auto_request.auto_tbl,
                                                auto_request.auto_request_post_tbl,
                                                auto_request.auto_request_sched_tbl)
            return
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
    """ Функция выполняет удаление завявки на проезд авто в ЛокалБД от сайта

    :param auto_request: AutoRequestSchema
    :param autoRequestService: AutoRequestService
    :return: JSONResponse
    """

    data = json.loads(auto_request.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if auto_request.token == '2332fasdfsd1234123sd213e21':
        if isinstance(auto_request.auto_request_tbl, AutoRequestTbl) and \
                isinstance(auto_request.auto_request_tbl.auto_request_id, int):
            autoRequestService.delete_auto_request(auto_request.auto_request_tbl)
            return
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
    """ Функция выполняет добавление записи в черный список в ЛокалБД от сайта

    :param blacklist: BlacklistSchema
    :param autoRequestService: BlacklistSchema
    :return: JSONResponse
    """

    data = json.loads(blacklist.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if blacklist.token == '2332fasdfsd1234123sd213e21':
        if isinstance(blacklist.secobjects_auto_blacklist_tbl, SecobjectsAutoBlacklistTbl) and \
                isinstance(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id, int):
            autoRequestService.add_blacklist(blacklist.secobjects_auto_blacklist_tbl)
            return
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
    """ Функция выполняет удаление авто из черного списка в ЛокалБД от сайта

    :param blacklist: BlacklistSchema
    :param autoRequestService: autoRequestService
    :return: JSONResponse
    """

    data = json.loads(blacklist.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if blacklist.token == '2332fasdfsd1234123sd213e21':
        if isinstance(blacklist.secobjects_auto_blacklist_tbl, SecobjectsAutoBlacklistTbl) and \
                isinstance(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id, int):
            autoRequestService.delete_blacklist(blacklist.secobjects_auto_blacklist_tbl.secobjects_auto_blacklist_id)
            return
        else:
            print({'detail': 'check input data for DELETE BL operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for DELETE BL operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)


@AutoRequestRouter.post(
    "/add_client/",
    status_code=status.HTTP_201_CREATED
)
def add_client(
        secobjects_tenant: SecobjectsTenantSchema,
        autoRequestService: AutoRequestService = Depends()):
    """ Функция выполняет добавление клиента в ЛокалБД от сайта

    :param secobjects_tenant: SecobjectsTenantSchema
    :param autoRequestService: AutoRequestService
    :return: JSONResponse
    """

    data = json.loads(secobjects_tenant.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if secobjects_tenant.token == '2332fasdfsd1234123sd213e21':
        if isinstance(secobjects_tenant.secobjects_tenant_tbl, SecobjectsTenantTbl):
            autoRequestService.add_client(secobjects_tenant.secobjects_tenant_tbl)
            return
        else:
            print({'detail': 'check input data for ADD LIMIT operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for ADD CLIENT operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)


@AutoRequestRouter.post(
    "/edit_client/",
    status_code=status.HTTP_201_CREATED
)
def edit_client(
        secobjects_tenant: SecobjectsTenantSchema,
        autoRequestService: AutoRequestService = Depends()):
    """ Функция выполняет редактирование клиента в ЛокалБД от сайта

    :param secobjects_tenant: SecobjectsTenantSchema
    :param autoRequestService: autoRequestService
    :return:
    """

    data = json.loads(secobjects_tenant.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if secobjects_tenant.token == '2332fasdfsd1234123sd213e21':
        if isinstance(secobjects_tenant.secobjects_tenant_tbl, SecobjectsTenantTbl):
            autoRequestService.edit_client(secobjects_tenant.secobjects_tenant_tbl)
            return
        else:
            print({'detail': 'check input data for EDIT LIMIT operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for EDIT CLIENT operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)


@AutoRequestRouter.post(
    "/del_client/",
    status_code=status.HTTP_201_CREATED
)
def del_client(
        secobjects_tenant: SecobjectsTenantSchema,
        autoRequestService: AutoRequestService = Depends()):
    """ Функция выполняет удаление клиента в ЛокалБД от сайта

    :param secobjects_tenant: SecobjectsTenantSchema
    :param autoRequestService: autoRequestService
    :return:
    """

    data = json.loads(secobjects_tenant.model_dump_json())
    print(f"data = {json.dumps(data)}")

    if secobjects_tenant.token == '2332fasdfsd1234123sd213e21':
        if isinstance(secobjects_tenant.secobjects_tenant_tbl, SecobjectsTenantTbl):
            autoRequestService.del_client(secobjects_tenant.secobjects_tenant_tbl)
            return
        else:
            print({'detail': 'check input data for EDIT LIMIT operation', 'data': data})
            return JSONResponse(content=jsonable_encoder({'detail': 'check input data for DEL CLIENT operation', 'data': data}),
                                status_code=status.HTTP_400_BAD_REQUEST)

