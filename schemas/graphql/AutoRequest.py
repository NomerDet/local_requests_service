import strawberry


@strawberry.type(description="Auto Request Schema")
class AutoRequestSchema:
    mode: str
    auto_request_id: int
    post_id: int
