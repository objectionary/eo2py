from __future__ import annotations
from abc import abstractmethod
from functools import partial


class EObase:
    @abstractmethod
    def dataize(self) -> object:
        raise NotImplementedError()


class EOerror(EObase):
    def __init__(self, msg):
        self.msg = msg

    def dataize(self) -> object:
        raise NotImplementedError(self.msg)


class EOboolean(EObase):
    def dataize(self) -> object:
        return self.value == "true"

    def __init__(self, value: str):
        self.value = value
        assert value.lower() == "true" or value.lower() == "false"
        self.If = partial(EOboolean_EOif, self)


class EOboolean_EOif(EObase):
    def __init__(self, condition: EOboolean, if_true: EObase, if_false: EObase):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def dataize(self) -> object:
        if self.condition.dataize():
            return self.if_true.dataize()
        else:
            return self.if_false.dataize()


class EOnumber(EObase):
    def __init__(self, value: int):
        self.value = value
        self.add = partial(EOint_EOadd, self)
        self.pow = partial(EOint_EOpow, self)
        self.sub = partial(EOint_EOsub, self)
        self.less = partial(EOnumber_EOless, self)

    def dataize(self) -> int:
        return self.value


class EOnumber_EOless(EOboolean):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__("false")
        self.parent = parent
        self.other = other

    def dataize(self) -> object:
        return self.parent.dataize() < self.other.dataize()


class EOint_EOadd(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() + self.other.dataize()


class EOint_EOsub(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() - self.other.dataize()


class EOint_EOpow(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() ** self.other.dataize()


def lazy_property(fn):
    attr_name = fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


if __name__ == "__main__":
    print(EOnumber(2).add(EOnumber(3).add(EOnumber(2))).dataize())

