class InputData:
    """
    get value from dict
    """
    d = {}

    def __init__(self, d):
        if d:
            self.d = d

    def get_int(self, key, default=None):
        """
        format int
        :param key:
        :param default:
        :return: int
        """
        return int(self.d.get(key)) if self.d.get(key) else default

    def get_str(self, key, default=None):
        """
        format str
        :param key:
        :param default:
        :return:
        """
        return str(self.d.get(key)) if self.d.get(key) else default

    def get_array(self, key, default=None):
        """
        format array
        :param key:
        :param default:
        :return:
        """
        return list(self.d.get(key)) if self.d.get(key) else default

    def pre_match_array(self, key, default=None):
        """
        format array
        :param key:
        :param default:
        :return:
        """
        result = []
        for _key, _value in self.d.items():
            if _key.startswith(key):
                result.append(_value)
        return result if result else default

    def get_array_by_str(self, key, sep, default=None):
        """
        str to array
        :param key:
        :param sep:
        :param default:
        :return:
        """
        return str(self.d.get(key)).split(sep) if self.d.get(key) else default

    def exists(self, key):
        """
        exists
        :param key:
        :return:
        """
        return key in self.d
