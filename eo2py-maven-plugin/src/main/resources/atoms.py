from __future__ import annotations
from abc import abstractmethod
from functools import partial


class EObase:
    @abstractmethod
    def dataize(self) -> object:
        raise NotImplementedError()


class EOattr(EObase, ):
    def __init__(self, obj, name, *args):
        self.obj = obj
        self.name = name
        self.args = args

    def dataize(self) -> object:
        if hasattr(self.obj, self.name):
            attr = getattr(self.obj, self.name)
            if callable(attr):
                return attr(*self.args).dataize()
            else:
                return attr.dataize()
        else:
            return getattr(self.obj.dataize(), self.name)(*self.args).dataize()


class EOerror(EObase, ):
    def dataize(self) -> object:
        raise NotImplementedError()


class EOnumber(EObase, ):
    def __init__(self, value: int):
        self.value = value
        self.add = partial(EOnumber_EOadd, self)
        self.sub = partial(EOnumber_EOsub, self)
        self.pow = partial(EOnumber_EOpow, self)
        self.less = partial(EOnumber_EOless, self)

    def dataize(self):
        return self

    def __eq__(self, other):
        return EObool("true" if self.value == other.value else "false")

    def __add__(self, other):
        return EOnumber(self.value + other.value)

    def __lt__(self, other):
        return EObool("true" if self.value < other.value else "false")

    def __sub__(self, other):
        return EOnumber(self.value - other.value)

    def __pow__(self, power, modulo=None):
        return EOnumber(self.value ** power.value)

    def __str__(self):
        return f"EOnumber({self.value})"


class EObool(EObase, ):
    def __init__(self, value: str):
        self.value = value
        self.If = partial(EObool_EOIf, self)

    def dataize(self) -> bool:
        return self

    def __bool__(self):
        return self.value == "true"

    def __str__(self):
        return f"EObool({self.__bool__()})"

    def __eq__(self, other):
        return EObool("true" if self.__bool__() == other.__bool__() else "false")


class EOnumber_EOadd(EOnumber, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() + self.other.dataize()


class EOnumber_EOsub(EOnumber, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() - self.other.dataize()


class EObool_EOIf(EObool, ):
    def __init__(self, parent: EObool, iftrue: EObase, iffalse: EObase):
        super().__init__("false")
        self.parent = parent
        self.iftrue = iftrue
        self.iffalse = iffalse

    def dataize(self):
        return self.iftrue.dataize() if self.parent.dataize() else self.iffalse.dataize()


class EOnumber_EOless(EObool, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__("false")
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() < self.other.dataize()


class EOnumber_EOpow(EOnumber, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() ** self.other.dataize()


def lazy_property(fn):
    attr = "_lazy__" + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr):
            value = fn(self)
            setattr(self, attr, value)
        return getattr(self, attr)

    return _lazy_property


if __name__ == "__main__":
    assert EOnumber(2) + EOnumber(3) == EOnumber(2).add(EOnumber(3)).dataize()
    assert EOnumber(2).sub(EOnumber(3)).dataize() == EOnumber(2) - EOnumber(3)
    assert EOnumber(2) ** EOnumber(3) == EOnumber(2).pow(EOnumber(3)).dataize()
    assert EObool("true") == EObool("true")
    assert EOnumber(2) < EOnumber(3)
    assert (EOnumber(2) < EOnumber(3)) == EOnumber(2).less(EOnumber(3)).dataize()

    assert EOattr(EOnumber(2), 'add', EOnumber(2)).dataize() == EOnumber(4)
    assert EOattr(EOnumber(2), 'add', EOattr(EOnumber(2), 'add', EOnumber(2))).dataize() == EOnumber(6)
    assert EOattr(EOattr(EOnumber(2), 'add', EOnumber(2)), 'add', EOnumber(2)).dataize() == EOnumber(6)
    dx = EOnumber(2)
    dy = EOnumber(2)
    dx_squared = EOattr(dx, 'pow', EOnumber(2))
    dy_squared = EOattr(dy, 'pow', EOnumber(2))
    dx_squared_plus_dy_squared = EOattr(dx_squared, 'add', dy_squared)
    sqrt_dx_squared_plus_dy_squared = EOattr(dx_squared_plus_dy_squared, 'pow', EOnumber(0.5))
    assert sqrt_dx_squared_plus_dy_squared.dataize() == EOnumber(8 ** 0.5)
