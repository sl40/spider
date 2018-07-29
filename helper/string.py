import hashlib


def merge_str(*args, dividing=':'):
    return dividing.join([str(_) for _ in args])


def sample_hash(s):
    """碰撞的可能性未知, 销量预测搬过来的
    :param s:
    :return:
    """
    m = hashlib.sha224()
    m.update(s.encode("utf8"))
    return int(m.hexdigest()[0:4], 16)
