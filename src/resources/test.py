# +package sandbox
#
# [n] > fibonacci
#   if. > @
#     n.less 3
#     small n
#     rec n 1 1
#
#   [n] > small
#     if. > @
#       n.eq 2
#       1
#       n
#
#   [n minus1 minus2] > rec
#     if. > @
#       n.eq 3
#       minus1.add minus2
#       rec (n.sub 1) (minus1.add minus2) minus1

class EOBase:
    def dataize(self):
        return None


class EOTrue(EOBase):
    def dataize(self):
        return True


class EOFalse(EOBase):
    def dataize(self):
        return False


class EOBoolean(EOBase):

    def __init__(self, value: EOBase):
        self.value = value

    def dataize(self):
        return self.value.dataize()


class EOIf(EOBase):
    def __init__(self, bool: EOBoolean, if_true: EOBase, if_false: EOBase):
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


class EOLess(EOBoolean):
    def __init__(self, left: EOInt, right: EOInt):
        super().__init__(EOTrue())
        self.left = left
        self.right = right

    def dataize(self):
        return self.left.dataize() < self.right.dataize()


class EOAdd(EOBase):
    def __init__(self, left: EOInt, right: EOInt):
        self.right = right
        self.left = left

    def dataize(self):
        left = self.left.dataize()
        right = self.right.dataize()
        result = left + right
        print(f"{left} + {right} = {result}")
        return result


class EOSub(EOInt):
    def __init__(self, left: EOInt, right: EOInt):
        super().__init__("0")
        self.right = right
        self.left = left

    def dataize(self):
        left = self.left.dataize()
        right = self.right.dataize()
        result = left - right
        print(f"{left} - {right} = {result}")
        return result


class Fibo(EOInt):
    def __init__(self, n):
        super().__init__("")
        self.n = n

    def dataize(self):
        n = self.n

        self.__PHI__ = EOIf(
            EOLess(n, EOInt("2")),
            n,
            EOAdd(
                Fibo(
                    EOSub(
                        n,
                        EOInt("1")
                    )),
                Fibo(
                    EOSub(
                        n,
                        EOInt("2")
                    ))
            )
        )

        return self.__PHI__.dataize()


print(Fibo(EOInt("11")).dataize())

#
# def decorator(func):
#     ABOBA = "ABOBA"
#     def wrapper(*args, **kwargs):
#         nonlocal ABOBA
#         print(ABOBA)
#         func(*args, **kwargs)
#
#     return wrapper
#
#
# @decorator
# def decoratee():
#     print("I am fucntion")
#
#
# decoratee()
