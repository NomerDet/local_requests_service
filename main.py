from fastapi import FastAPI, Request, status

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from config.GraphQL import get_graphql_context
from metadata.Tags import Tags
from models.BaseModel import init
from routers.v1.AutoRequestRouter import AutoRequestRouter
from schemas.graphql.Query import Query
from middleware.middleware import MyMiddleware

# Application Environment Configuration
DEBUG_MODE = True

# Core Application Instance
app = FastAPI(
    # title=env.APP_NAME,
    # version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Middleware
app.add_middleware(MyMiddleware, some_attribute="some_attribute_here_if_needed")

# Add Routers
app.include_router(AutoRequestRouter)

# GraphQL Schema and Application Instance
schema = Schema(query=Query)
graphql = GraphQLRouter(
    schema,
    graphiql=DEBUG_MODE,
    context_getter=get_graphql_context,
)

# Integrate GraphQL Application to the Core one
app.include_router(
    graphql,
    prefix="/graphql",
    include_in_schema=False,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        error['msg'].replace('None', error['loc'][-1])
    return JSONResponse(content=jsonable_encoder({"detail": exc.errors()}),
                        status_code=status.HTTP_400_BAD_REQUEST)

# Initialise Data Model Attributes
init()
