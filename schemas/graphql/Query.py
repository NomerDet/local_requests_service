import strawberry
from strawberry.types import Info

from config.GraphQL import (
    get_AutoRequestService,
)


@strawberry.type(description="Query all entities")
class Query:

    @strawberry.field(description="Check an Auto Request")
    def auto_request(
            self, req_id: int, post_id: int, mode: str, number: str, info: Info
    ) -> bool:
        autoRequestService = get_AutoRequestService(info)
        if mode == 'auto_request_enter':
            return autoRequestService.check_auto_request_enter(req_id, post_id, number)
        else:
            return autoRequestService.check_auto_request_leave(req_id, post_id, number)
