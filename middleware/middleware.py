import json

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class
class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    # https://stackoverflow.com/questions/69669808/fastapi-custom-middleware-getting-body-of-request-inside
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):
        # если GET запрос и ['/v1/auto_request/check', '/v1/auto_request/spec'] в url запроса
        if request.method == 'GET' and request.url.path in ['/v1/auto_request/check', '/v1/auto_request/spec', '/v1/auto_request/check/', '/v1/auto_request/spec/']:
            # process the request and get the response
            print('process the request and get the response')
            response = await call_next(request)
            return response

        # do something with the request object, for example
        await self.set_body(request)
        # https://stackoverflow.com/questions/73278844/how-to-inspect-every-request-including-request-body-with-fastapi
        try:
            jsonbody = await request.json()
            # если токен от сайта корректный и работает с POST запросом
            # TODO: вынести в конфиг
            if jsonbody.get('token', '') == '2332fasdfsd1234123sd213e21':
                # process the request and get the response
                response = await call_next(request)
                return response
            else:
                print("token issue")
                return JSONResponse(
                    status_code=400,
                    content={'message': 'Incorrect token!'},
                )
        except json.decoder.JSONDecodeError:
            return JSONResponse(
                status_code=400,
                content={'message': 'Only POST methods allowed!'},
            )

