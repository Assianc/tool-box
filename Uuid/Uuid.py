import uuid


def generate_uuid():
    """
    生成一个随机的UUIDv4字符串。

    Returns:
      str: 生成的UUIDv4字符串。
    """

    return str(uuid.uuid4())


if __name__ == "__main__":
    print(generate_uuid())
