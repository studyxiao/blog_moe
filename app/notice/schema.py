from pydantic import validator

from app.core.schema import PageSchema


class NoticeListSchema(PageSchema):
    status: int | None

    @validator("status")
    def check_status(cls, val: int | None) -> int | None:
        if val is None or val <= 0:
            return None
        if val not in [0, 1]:
            raise ValueError("通知类型 0-未读 1-已读")
        return val
