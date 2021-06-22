from __future__ import annotations
from abc import abstractmethod
from functools import partial


class EObase:
    @abstractmethod
    def dataize(self) -> object:
        raise NotImplementedError()


class EOerror(EObase):
    def dataize(self) -> object:
        raise NotImplementedError()


class EOnumber(EObase):
    def __init__(self, value: int):
        self.value = value
        self.add = partial(EOnumber_EOadd, self)
        self.sub = partial(EOnumber_EOsub, self)
        self.pow = partial(EOnumber_EOpow, self)
        self.less = partial(EOnumber_EOless, self)

    def dataize(self) -> int:
        return self.value


class EObool(EObase):
    def __init__(self, value: bool):
        self.value = value
        self.If = partial(EObool_If, self)

    def dataize(self) -> bool:
        return self.value


class EOnumber_EOadd(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() + self.other.dataize()


class EOnumber_EOsub(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() - self.other.dataize()



class EObool_If(EObase):
    def __init__(self, parent: EObool, iftrue: EObase, iffalse: EObase):
        self.parent = parent
        self.iftrue = iftrue
        self.iffalse = iffalse

    def dataize(self):
        return self.iftrue.dataize() if self.parent.dataize() else self.iffalse.dataize()


class EOnumber_EOless(EObool):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(False)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() < self.other.dataize()


class EOnumber_EOpow(EOnumber):
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
    print(EOnumber(2).pow(EOnumber(10)).dataize())
