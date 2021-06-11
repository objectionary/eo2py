from abc import abstractmethod


class EOBase:
    @abstractmethod
    def dataize(self) -> object:
        return None


class DataizationException(Exception):
    pass


class EOError(EOBase):
    def __init__(self, msg):
        self.msg = msg

    def dataize(self):
        raise DataizationException(self.msg)


class EOBoolean(EOBase):
    def __init__(self, value: str):
        if value.lower() == "true" or value.lower() == "false":
            self.value = value
        else:
            raise TypeError("String parameter should be either 'true' or 'false'")

    def dataize(self):
        return self.value == "true"


class EOIf(EOBase):
    def __init__(self, bool: EOBase, if_true: EOBase, if_false: EOBase):
        self.bool = bool
        self.if_true = if_true
        self.if_false = if_false

    def dataize(self):
        if self.bool.dataize():
            return self.if_true.dataize()
        else:
            return self.if_false.dataize()


# print(
#     EOIf(
#         EOBoolean(EOFalse()),
#         EOTrue(),
#         EOFalse()
# ).dataize())

class EOInt(EOBase):
    def __init__(self, string: str):
        self.value = string

    def dataize(self):
        return int(self.value)


class EOLess(EOBase):
    def __init__(self, left: EOBase, right: EOBase):
        self.left = left
        self.right = right

    def dataize(self):
        return self.left.dataize() < self.right.dataize()


class EOAdd(EOBase):
    def __init__(self, left: EOBase, right: EOBase):
        self.right = right
        self.left = left

    def dataize(self):
        left = self.left.dataize()
        right = self.right.dataize()
        result = left + right
        # print(f"{left} + {right} = {result}")
        return result


class EOSub(EOBase):
    def __init__(self, left: EOBase, right: EOBase):
        self.right = right
        self.left = left

    def dataize(self):
        left = self.left.dataize()
        right = self.right.dataize()
        result = left - right
        # print(f"{left} - {right} = {result}")
        return result
