from flask import Blueprint
from flask.typing import ResponseReturnValue
from sqlalchemy import or_, select

from app.article.model import Article, ArticleLike, Category, Comment, Tag
from app.article.shema import (
    ArticleCreateSchema,
    ArticleListSchema,
    CategorySchema,
    CommentListSchema,
    CommentSchema,
    FilterSchema,
    TagSchema,
)
from app.core.auth.model import User
from app.core.auth.permission import admin_required, current_user, login_required
from app.core.exception import Created, Deleted, ParameterException, Unauthorized
from app.core.model import session
from app.core.schema import validate
from app.core.schema.common import PageSchema, ResultPageSchema
from app.util.const import Publish

bp = Blueprint("article", __name__, url_prefix="/article")


@bp.get("")
@login_required(optional=True)
@validate
def get_article_list(query: ArticleListSchema) -> ResponseReturnValue:
    """获取文章列表."""
    user = current_user.get()

    page = query.page
    count = query.count
    _query = [Article.is_deleted == 0]
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


@bp.get("/<int:article_id>")
@login_required(optional=True)
def get_article(article_id: int) -> ResponseReturnValue:
    """获取文章详情."""
    user = current_user.get()
    article = Article.get_by_id(article_id)
    if article is None or article.is_deleted:
        raise ParameterException(message="文章不存在")
    if user is None:
        if article.publish != Publish.PUBLISH.value:  # 未登录不能查看非公开文章
            raise ParameterException(message="文章不存在")
    else:
        if article.publish == 2 and article.user_id != user.id:  # 登录但不是作者不能查看文章
            raise ParameterException(message="文章不存在")
    return article.to_dict()


@bp.put("/<int:article_id>")
@login_required
@validate
def update_article(article_id: int, body: ArticleCreateSchema) -> ResponseReturnValue:
    """更新文章."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    article = Article.get_by_id(article_id)
    if article is None or article.is_deleted:
        raise ParameterException(message="文章不存在")
    if article.user_id != user.id:
        raise ParameterException(message="文章不存在")
    if body.summary is None:
        body.summary = body.content[:200]
    data = body.dict(exclude_none=True)
    data.pop("title")
    article = article.update_by_self(data)
    article.save()
    return article.to_dict()


@bp.delete("/<int:article_id>")
@login_required
def delete_article(article_id: int) -> ResponseReturnValue:
    """删除文章."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    article = Article.get_by_id(article_id)
    if article is None or article.is_deleted:
        raise ParameterException(message="文章不存在")
    if article.user_id != user.id:
        raise ParameterException(message="文章不存在")
    article.is_deleted = True
    article.save()
    return Deleted(message="删除成功")


@bp.get("/category")
def get_category() -> ResponseReturnValue:
    """获取文章分类."""
    categories = Category.get_all()
    res = [
        {
            "id": 0,
            "name": "默认分类",
        }
    ]
    res.extend([category.to_dict() for category in categories])
    return res


@bp.post("/category")
@admin_required
@validate
def create_category(body: CategorySchema) -> ResponseReturnValue:
    """创建文章分类."""
    category = Category.get_by_attr(Category.name == body.name)
    if category:
        return category.to_dict()
    category = Category(name=body.name).save()
    return category.to_dict()


@bp.put("/category/<int:category_id>")
@admin_required
@validate
def update_category(category_id: int, body: CategorySchema) -> ResponseReturnValue:
    """更新文章分类."""
    category = Category.get_by_id(category_id)
    if category is None:
        raise ParameterException(message="分类不存在")
    category.name = body.name
    category.save()
    return category.to_dict()


@bp.delete("/category/<int:category_id>")
@admin_required
def delete_category(category_id: int) -> ResponseReturnValue:
    """删除文章分类."""
    category = Category.get_by_id(category_id)
    if category is None:
        raise ParameterException(message="分类不存在")
    articles = Article.get_all(category_id=category_id)
    for article in articles:
        # 将文章分类设置为默认分类
        article.category_id = 0
        article.save()
    category.delete_by_self()
    return Deleted(message="删除成功")


@bp.get("/tag")
@validate
def get_tag(query: TagSchema) -> ResponseReturnValue:
    """获取文章标签."""
    with session:
        res = session.scalars(select(Tag).where((Tag.name).like(f"%{query.name}%")).limit(10)).all()
        return list(res)


@bp.post("/tag")
@login_required
@validate
def create_tag(body: TagSchema) -> ResponseReturnValue:
    """创建文章标签."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    tag = Tag.get_by_attr(Tag.name == body.name)
    if tag:
        return tag.to_dict()
    tag = Tag(name=body.name).save()
    return tag.to_dict()


@bp.post("/<int:article_id>/like")
@login_required
def like_article(article_id: int) -> ResponseReturnValue:
    """点赞文章."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    article = Article.get_by_id(article_id)
    if article is None or article.is_deleted:
        raise ParameterException(message="文章不存在")
    liked = ArticleLike.get_by_attr(ArticleLike.article_id == article_id, ArticleLike.user_id == user.id)
    if liked:
        liked.delete_by_self()
        return Deleted(message="取消点赞成功")
    ArticleLike(article_id=article_id, user_id=user.id).save()
    # TODO 通知作者
    return Created(message="点赞成功")


@bp.get("archive")
@login_required(optional=True)
@validate
def get_archive(query: PageSchema) -> ResponseReturnValue:
    """获取文章归档."""
    user = current_user.get()
    _query = [Article.is_deleted == 0]
    if user is None:
        # 未登录用户只能看公开的文章
        _query.append(Article.publish == 1)
    articles = Article.get_all(
        query.page,
        query.count,
        *_query,
    )
    exclude_field = {"content", "category_id", "user_id", "tags", "cover", "is_deleted"}
    items = [article.to_dict(exclude_field=exclude_field) for article in articles]
    return ResultPageSchema(
        items=items,
        page=1,
        count=1000,
        total=User.count(
            *_query,
        ),
    ).dict()


@bp.get("/my")
@login_required
@validate
def get_my_article(query: PageSchema) -> ResponseReturnValue:
    """获取我的文章."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    articles = Article.get_all(
        query.page,
        query.count,
        Article.user_id == user.id,
        Article.is_deleted == 0,
    )
    exclude_field = {"content", "category_id", "user_id", "cover", "is_deleted"}
    items = [article.to_dict(exclude_field=exclude_field) for article in articles]
    return ResultPageSchema(
        items=items,
        page=query.page,
        count=query.count,
        total=Article.count(
            Article.user_id == user.id,
            Article.is_deleted == 0,
        ),
    ).dict()


@bp.get("/<int:article_id>/comment")
@validate
def get_article_comment(article_id: int, query: CommentListSchema) -> ResponseReturnValue:
    """获取文章评论."""
    if query.root_id:
        # 子评论
        root = Comment.get_by_attr(
            Comment.id == query.root_id,
            Comment.article_id == article_id,
            Comment.root_id == 0,
        )
        if root is None:
            raise ParameterException(message="评论不存在")
        comments = Comment.get_children_by_root_id(query.root_id, query.page, query.count)
        total = Comment.count(Comment.root_id == query.root_id, is_deleted=0)
        return ResultPageSchema(
            items=comments,
            page=query.page,
            count=query.count,
            total=total,
        ).dict()
    comments = Comment.get_comment_by_article_id(article_id, query.page, query.count)
    total = Comment.count(Comment.article_id == article_id, is_deleted=0)
    return ResultPageSchema(
        items=comments,
        page=query.page,
        count=query.count,
        total=total,
    ).dict()


@bp.post("/<int:article_id>/comment")
@login_required
@validate
def create_article_comment(article_id: int, body: CommentSchema) -> ResponseReturnValue:
    """创建文章评论."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="请先登录")
    article = Article.get_by_id(article_id)
    if article is None or article.is_deleted:
        raise ParameterException(message="文章不存在")
    if body.parent_id:
        parent = Comment.get_by_id(body.parent_id)
        if parent is None or parent.is_deleted:
            raise ParameterException(message="父评论不存在")
    if body.root_id:
        root = Comment.get_by_id(body.root_id)
        if root is None or root.is_deleted:
            raise ParameterException(message="根评论不存在")
    _query = {}
    if body.root_id:
        _query["root_id"] = body.root_id
        if body.parent_id is None:
            _query["parent_id"] = body.root_id
    if body.parent_id:
        _query["parent_id"] = body.parent_id
    comment = Comment(
        article_id=article_id,
        user_id=user.id,
        content=body.content,
        **_query,
    ).save()
    return comment.to_dict()
