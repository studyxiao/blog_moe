from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import TEXT, Index, String, delete, select
from sqlalchemy.orm import Mapped, mapped_column

from app.core.auth.model import User
from app.core.model import BaseModel, T_create_time, T_update_time, session

if TYPE_CHECKING:
    from app.article.shema import TagSchema


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String(32), unique=True, comment="分类名称")
    info: Mapped[str] = mapped_column(String(200), default=None, comment="描述")
    banner: Mapped[str] = mapped_column(String(255), default=None, comment="背景图")
    sort: Mapped[int] = mapped_column(default=1, comment="排序")
    status: Mapped[int] = mapped_column(default=1, comment="状态: 1可见, 0-不可见")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)
    update_time: Mapped[T_update_time] = mapped_column(default_factory=datetime.utcnow)
    is_deleted: Mapped[int] = mapped_column(default=0, comment="是否删除, 0-未删除, 1-已删除")

    __tableargs__ = (Index("name_del", "name", "is_deleted", unique=True),)


class Tag(BaseModel):
    name: Mapped[str] = mapped_column(String(32), comment="标签名称")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)


class ArticleTag(BaseModel):
    article_id: Mapped[int] = mapped_column(comment="文章 id")
    tag_id: Mapped[int] = mapped_column(comment="tag id")


class ArticleLike(BaseModel):
    user_id: Mapped[int] = mapped_column(comment="用户 id")
    article_id: Mapped[int] = mapped_column(comment="文章 id")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)


class Article(BaseModel):
    title: Mapped[str] = mapped_column(String(128), comment="文章标题")
    summary: Mapped[str] = mapped_column(String(255), comment="简介")
    content: Mapped[str] = mapped_column(TEXT, comment="文章内容")
    user_id: Mapped[int] = mapped_column(comment="作者 id")
    cover: Mapped[str] = mapped_column(String(255), default=None, comment="头图 url")
    category_id: Mapped[int] = mapped_column(default=0, comment="所属分类 id,  0 表示没有分类")
    source: Mapped[int] = mapped_column(default=1, comment="来源: 1-原创, 2-转载, 3-翻译")
    publish: Mapped[int] = mapped_column(default=1, comment="可见范围: 1-公开, 2-登录, 3-仅自己")
    status: Mapped[int] = mapped_column(default=1, comment="状态: 1可见, 0-不可见,2-作者置顶, 3-管理员置顶")
    sort: Mapped[int] = mapped_column(default=1, comment="排序")
    allow_comment: Mapped[int] = mapped_column(default=1, comment="是否允许评论: 1-允许, 0-不允许")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)
    update_time: Mapped[T_update_time] = mapped_column(default_factory=datetime.utcnow)
    is_deleted: Mapped[int] = mapped_column(default=0, nullable=False, comment="是否删除,0-未删除, 1-已删除")

    # TODO view_count: Mapped[int] = mapped_column(default=0, comment="文章浏览量")
    # TODO like_count: Mapped[int] = mapped_column(default=0, comment="点赞量")
    # TODO comment_count: Mapped[int] = mapped_column(default=0, comment="评论数")

    __tableargs__ = (Index("name", "name"), Index("status", "status"))

    @property
    def tags(self) -> list[Tag]:
        res = []
        with session:
            _tags = session.scalars(select(ArticleTag.tag_id).where(ArticleTag.article_id == self.id)).all()
            for tag_id in _tags:
                tag = Tag.get_by_id(tag_id)
                if tag is not None:
                    res.append(tag)

        return res

    @tags.setter
    def tags(self, data: list["TagSchema"]) -> None:
        with session:
            new_tags = set()
            old_tags = set()
            for item in data:
                _tag = Tag.get_by_attr(name=item.name)
                if _tag is None:
                    _tag = Tag(name=item.name)
                    session.add(_tag)
                    session.refresh(_tag)
                new_tags.add(_tag.id)
            _tags = session.scalars(select(ArticleTag).where(ArticleTag.article_id == self.id)).all()
            old_tags.update(tag.tag_id for tag in _tags)
            in_tags = new_tags - old_tags
            out_tags = old_tags - new_tags
            for in_tag in in_tags:
                article_tag = ArticleTag(article_id=self.id, tag_id=in_tag)
                session.add(article_tag)
            for out_tag in out_tags:
                session.execute(
                    delete(ArticleTag).where(ArticleTag.article_id == self.id, ArticleTag.tag_id == out_tag)
                )
            session.commit()

    @property
    def category(self) -> dict[str, Any]:
        cate = {"id": 0, "name": "默认分类"}
        if self.category_id > 0:
            res = Category.get_by_id(self.category_id)
            if res:
                cate = {"id": res.id, "name": res.name}
        return cate

    @property
    def user(self) -> dict[str, Any]:
        user = User.get_by_id(self.user_id)
        if user is None:
            return {}
        return {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
        }


class File(BaseModel):
    """暂时不需要."""

    __abstract__ = True
    md5: Mapped[str] = mapped_column(comment="唯一标识")
    user_id: Mapped[int] = mapped_column(comment="用户 id")
    path: Mapped[str] = mapped_column(String(100), comment="路径或 url")
    name: Mapped[str] = mapped_column(comment="名称")
    location: Mapped[int] = mapped_column(default=1, comment="文件保存位置: 1-本地, 2-云")
    type: Mapped[int] = mapped_column(default=0, comment="文件类型: 0-未知, 1-图片, 2-视频, 3-音频")  # noqa：A003
    ext: Mapped[str] | None = mapped_column(default=None, comment="后缀")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)
    update_time: Mapped[T_update_time] = mapped_column(default_factory=datetime.utcnow)

    __tableargs__ = (Index("user_file", "user_id", "md5"),)


class Comment(BaseModel):
    article_id: Mapped[int]
    user_id: Mapped[int]
    content: Mapped[str] = mapped_column(String(400), comment="评论内容")
    root_id: Mapped[int] = mapped_column(default=0, comment="所属根评论 id, 0表示本身就是根评论")
    parent_id: Mapped[int] = mapped_column(default=0, comment="所属父评论 id, 0-表示本身就是根评论, 没有父级")
    replay_count: Mapped[int] = mapped_column(default=0, comment="如果是 root, 需要统计它的回复数量")

    ip: Mapped[str] = mapped_column(String(16), default=None, comment="ip 地址")
    platform: Mapped[str] = mapped_column(String(20), default="", comment="客户端")
    device: Mapped[str] = mapped_column(String(20), default="", comment="设备")

    status: Mapped[int] = mapped_column(default=1, comment="状态: 1-正常, 0-不显示, 2-作者置顶, 3-管理员置顶")
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)
    is_deleted: Mapped[int] = mapped_column(default=0, comment="是否删除,0-未删除, 1-已删除")


class CommentLike(BaseModel):
    user_id: Mapped[int] = mapped_column()
    comment_id: Mapped[int] = mapped_column()
    create_time: Mapped[T_create_time] = mapped_column(default_factory=datetime.utcnow)
