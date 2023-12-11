from fastapi import Depends
from strawberry.types import Info

from services.AutoRequestService import AutoRequestService


# GraphQL Dependency Context
async def get_graphql_context(
        autoRequestService: AutoRequestService = Depends(),
):
    return {
        "autoRequestService": autoRequestService,
    }


# Extract BookService instance from GraphQL context
def get_AutoRequestService(info: Info) -> AutoRequestService:
    return info.context["autoRequestService"]
