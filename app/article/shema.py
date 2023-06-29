from datetime import date
from typing import Any

from pydantic import BaseModel, validator

from app.article.controller import category_existed, create_tag, tag_existed
from app.core.schema import PageSchema
from app.user.model import user_existed
from app.util.const import Source


class FilterSchema(BaseModel):
    tag_id: int | None
    category_id: int | None
    user_id: int | None
    source: int | None


class DateFilterSchema(BaseModel):
    start_date: date | None
    end_date: date | None


class ArticleListSchema(PageSchema):
    tag_id: int | None
    category_id: int | None
    user_id: int | None
    source: int | None
    start_date: date | None
    end_date: date | None

    @validator("tag_id")
    def check_tag_id(cls, val: int | None) -> int | None:
        if val is None or val <= 0:
            return None
        if not tag_existed(val):
            raise ValueError("标签不存在")
        return val

    @validator("category_id")
    def check_category_id(cls, val: int | None) -> int | None:
        if val is None or val <= 0:
            return None
        if not category_existed(val):
            raise ValueError("分类不存在")
        return val

    @validator("user_id")
    def check_user_id(cls, val: int | None) -> int | None:
        if val is None or val <= 0:
            return None
        if not user_existed(val):
            raise ValueError("作者不存在")
        return val

    @validator("source")
    def check_source(cls, val: int | None) -> int | None:
        if val is None or val <= 0:
            return None
        if val not in Source.__members__.values():
            raise ValueError("来源不存在")
        return val

    @validator("start_date")
    def check_start_date(cls, val: date | None, values: dict[str, Any]) -> date | None:
        if val is None or val < date(2023, 1, 1):
            return None
        if (end := values.get("end_date")) and val > end:
            raise ValueError("开始日期不能大于结束日期")
        return val

    @validator("end_date")
    def check_end_date(cls, val: date | None, values: dict[str, date]) -> date | None:
        if val is None or val < date(2023, 1, 1):
            return None
        if (start := values.get("start_date")) and val < start:
            raise ValueError("结束日期不能小于开始日期")
        return val


class TagSchema(BaseModel):
    id: int | None
    name: str


class ArticleCreateSchema(BaseModel):
    title: str
    content: str
    summary: str | None
    cover: str | None
    category_id: int = 0
    tags: list[TagSchema] | None
    publish: int = 1
    source: int = Source.YUANCHUANG.value

    @validator("title")
    def check_title(cls, val: str) -> str:
        if not val or val.strip() == "":
            raise ValueError("标题不能为空")
        return val

    @validator("content")
    def check_content(cls, val: str) -> str:
        if not val or val.strip() == "":
            raise ValueError("内容不能为空")
        return val

    @validator("summary")
    def check_summary(cls, val: str | None, values: dict[str, Any]) -> str | None:
        if val is None or val.strip() == "":
            return values.get("content", "")[:100]
        return val

    @validator("cover")
    def check_cover(cls, val: str | None) -> str | None:
        if val is None or val.strip() == "":
            return None
        if not val.startswith(("http://", "https://")):
            raise ValueError("封面地址不合法")
        return val

    @validator("category_id")
    def check_category_id(cls, val: int) -> int:
        if val == 0:
            # 默认分类
            return val
        if not category_existed(val):
            raise ValueError("分类不存在")
        return val

    @validator("tags")
    def check_tags(cls, val: list[TagSchema] | None) -> list[TagSchema]:
        if val is None:
            return []
        res = []
        for tag in val:
            if tag.id is not None:
                if not tag_existed(tag.id):
                    raise ValueError(f"标签{tag.name}不存在")
                res.append(tag)
            else:
                # 创建标签
                _tag = create_tag(tag.name)
                res.append(_tag)
        return res

    @validator("publish")
    def check_publish(cls, val: int) -> int:
        if val not in [0, 1, 2]:
            raise ValueError("发布状态不存在")
        return val

    @validator("source")
    def check_source(cls, val: int) -> int:
        if val not in Source.__members__.values():
            raise ValueError("来源不存在")
        return val
