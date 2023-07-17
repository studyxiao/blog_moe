from flask import Blueprint
from flask.typing import ResponseReturnValue

from app.core.auth import current_user, login_required
from app.core.exception import Forbidden, ParameterException, Success, Unauthorized
from app.core.model import session
from app.core.schema.schema import validate
from app.notice.schema import NoticeListSchema

from .model import Notice

bp = Blueprint("notice", __name__, url_prefix="/notice")


@bp.get("")
@login_required
@validate
def get_notice(query: NoticeListSchema) -> ResponseReturnValue:
    """获取通知列表."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="用户不存在")
    _query = [Notice.to_user_id == user.id]
    if query.status is not None:
        _query.append(Notice.status == query.status)
    notices = Notice.get_all(query.page, query.count, *_query)
    res = []
    for notice in notices:
        res.append(notice.to_dict())
    return res


@bp.put("/<int:notice_id>")
@login_required
def update_notice(notice_id: int) -> ResponseReturnValue:
    """更新通知状态."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="用户不存在")
    notice = Notice.get_by_id(notice_id)
    if notice is None:
        raise ParameterException(message="通知不存在")
    if notice.to_user_id != user.id:
        raise Forbidden(message="无权操作")
    notice.status = 1
    notice.update()
    return notice.to_dict()


@bp.put("/all")
@login_required
def update_all_notice() -> ResponseReturnValue:
    """更新所有通知状态."""
    user = current_user.get()
    if user is None:
        raise Unauthorized(message="用户不存在")
    with session:
        Notice.update().where(Notice.to_user_id == user.id).values(status=1)
        session.commit()
    return Success(message="所有通知已读")
