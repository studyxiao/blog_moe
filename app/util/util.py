import secrets
import string


def generate_digit_code(size: int = 6) -> str:
    """生成数字类型随机验证码.

    Args:
        size (int, optional): 字符个数. Defaults to 6.

    Returns:
        str: 验证码
    """
    words = string.digits
    return "".join(secrets.choice(words) for _ in range(size))
