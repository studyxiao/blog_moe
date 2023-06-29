from flask import Blueprint
from flask.typing import ResponseReturnValue
from sqlalchemy import or_

from app.article.model import Article
from app.article.shema import ArticleCreateSchema, ArticleListSchema, FilterSchema
from app.core.auth.model import User
from app.core.auth.permission import current_user, login_required
from app.core.exception import Unauthorized
from app.core.schema import validate
from app.core.schema.common import ResultPageSchema

bp = Blueprint("article", __name__, url_prefix="/article")


@bp.get("")
@login_required(optional=True)
@validate
def get_article_list(query: ArticleListSchema) -> ResponseReturnValue:
    """获取文章列表."""
    user = current_user.get()

    page = query.page
    count = query.count
    _query = []
    if query.start_date:
        _query.append(Article.create_time >= query.start_date)
    if query.end_date:
        _query.append(Article.create_time <= query.end_date)
    if user:
        # 登录用户可以看到公开的文章、登录可见文章、自己的文章
        _query.append(or_(Article.publish.in_([1, 2]), Article.user_id == user.id))
    else:
        # 未登录用户只能看公开的文章
        _query.append(Article.publish == 1)
    filter_fields = FilterSchema.parse_obj(query.dict(exclude_none=True))

    articles = Article.get_all(
        page,
        count,
        *_query,
        **filter_fields.dict(exclude_none=True),
    )
    items = [article.to_dict(exclude_field={"category_id", "user_id"}) for article in articles]
    return ResultPageSchema(
        items=items,
        page=page,
        count=count,
        total=User.count(
            *_query,
            **filter_fields.dict(exclude_none=True),
        ),
    ).dict()


@bp.post("")
@login_required
@validate
def create_article(body: ArticleCreateSchema) -> ResponseReturnValue:
    """创建文章."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    # if user.role_id < 2:  # TODO 硬编码修改
    #     # 1为普通用户,2为撰稿者
    #   E  raise Unauthorized(message="权限不足") #
    if body.summary is None:
        body.summary = body.content[:200]
    data = body.dict(exclude_none=True)
    tags = data.pop("tags")
    article = Article(
        **data,
        user_id=user.id,
    ).save()
    if body.tags:
        article.tags = tags
    article.save()
    return article.to_dict()
