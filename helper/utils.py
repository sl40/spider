from math import ceil


def generator_page(count, page_size, start=1):
    for page in range(start, int(ceil(count/page_size))+1):
        yield page


def generator_list(l, page_size, start=1):
    _list = list(l)
    for page in range(start, int(ceil(len(_list)/page_size)+1)):
        yield _list[(page-1)*page_size:page*page_size]


def number_to_any_str(n, s='01234'):
    base = len(s)
    if n < base:
        return s[n]
    else:
        return number_to_any_str(n // base, s) + s[n % base]


def random_copy(s):
    s1 = s
    s2 = s[::-1]
    result = ''
    for _index, _value in enumerate(s1):
        result += _value * int(s2[_index])
    return result


def division(a, b, multiple=100, default=0, ndigits=2):
    """
    除法计算
    :param double a:
    :param double b:
    :param double multiple:
    :param double default:
    :param ndigits:
    :return:
    """
    return round(a / b * multiple, ndigits) if b > 0 else default