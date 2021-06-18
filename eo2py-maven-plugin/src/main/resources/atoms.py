from __future__ import annotations
from abc import abstractmethod
from functools import partial


class EOmeta(type):

    def __call__(cls, *args, **kwargs):
        def resolve_attribute(obj, attr_name):
            try:
                return object.__getattribute__(obj, attr_name)
            except AttributeError:
                __PHI__ = object.__getattribute__(obj, '__PHI__')
                return getattr(__PHI__, attr_name)

        cls.__getattribute__ = resolve_attribute

        new_obj = cls.__new__(cls, *args, **kwargs)
        object.__getattribute__(new_obj, '__init__')(*args, **kwargs)
        return new_obj


class EObase(metaclass=EOmeta):
    @abstractmethod
    def dataize(self) -> object:
        raise NotImplementedError()


class EOattr(EObase, metaclass=EOmeta):
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name

    def dataize(self) -> object:
        return getattr(self.cls, self.name).dataize()

    def __call__(self, *args, **kwargs):
        return getattr(self.cls, self.name)(*args, **kwargs)


class EOapp(EObase):
    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return object.__getattribute__(self.cls(*self.args), item)

    def __init__(self, cls, *args):
        self.cls = cls
        self.args = args

    def dataize(self) -> object:
        return self.cls(*self.args).dataize()


class EOerror(EObase, metaclass=EOmeta):
    def dataize(self) -> object:
        raise NotImplementedError()


class EOnumber(EObase, metaclass=EOmeta):
    def __init__(self, value: int):
        self.value = value
        self.add = partial(EOnumber_EOadd, self)
        self.sub = partial(EOnumber_EOsub, self)
        self.pow = partial(EOnumber_EOpow, self)
        self.less = partial(EOnumber_EOless, self)

    def dataize(self) -> int:
        return self.value


class EObool(EObase, metaclass=EOmeta):
    def __init__(self, value: bool):
        self.value = value
        self.If = partial(EObool_If, self)

    def dataize(self) -> bool:
        return self.value


class EOnumber_EOadd(EOnumber, metaclass=EOmeta):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() + self.other.dataize()


class EOnumber_EOsub(EOnumber, metaclass=EOmeta):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() - self.other.dataize()


class EObool_If(EObase, metaclass=EOmeta):
    def __init__(self, parent: EObool, iftrue: EObase, iffalse: EObase):
        self.parent = parent
        self.iftrue = iftrue
        self.iffalse = iffalse

    def dataize(self):
        return self.iftrue.dataize() if self.parent.dataize() else self.iffalse.dataize()


class EOnumber_EOless(EObool, metaclass=EOmeta):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(False)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() < self.other.dataize()


class EOnumber_EOpow(EOnumber, metaclass=EOmeta):
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
