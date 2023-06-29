from .model import Category, Tag


def tag_existed(tag_id: int) -> bool:
    # 暂时不缓存
    return bool(Tag.get_by_id(tag_id))


def category_existed(category_id: int) -> bool:
    # 暂时不缓存
    return bool(Category.get_by_id(category_id))


def create_tag(name: str) -> Tag:
    tag = Tag.get_by_attr(Tag.name == name)
    if tag:
        return tag
    return Tag(name=name).save()
