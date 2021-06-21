from __future__ import annotations
from abc import abstractmethod
from functools import partial


class EObase:
    @abstractmethod
    def dataize(self) -> EObase:
        raise NotImplementedError()


class EOattr(EObase, ):
    def __init__(self, obj, name, *args):
        self.obj = obj
        self.name = name
        self.args = args

    def __str__(self):
        return f"{self.obj}.{self.name}"

    def dataize(self) -> object:
        attr = None
        if hasattr(self.obj, self.name):
            print(f"Found .{self.name} in {self.obj}.")
            attr = getattr(self.obj, self.name)
        elif hasattr(self.obj, '__PHI__') and hasattr(self.obj.__PHI__, self.name):
            print(f"Did not find .{self.name} in {self.obj}, found .{self.name} in {self.obj.__PHI__}.")
            attr = getattr(self.obj.__PHI__, self.name)
        else:
            print(f"Attribute .{self.name} was not found. Dataizing {self.obj}...")

        if attr is not None:
            if callable(attr):
                print(f"Dataizing {attr} applied to {[str(arg) for arg in self.args]}.")
                return attr(*self.args).dataize()
            else:
                print(f"Dataizing {attr}, no args needed.")
                return attr.dataize()

        return getattr(self.obj.dataize(), self.name)(*self.args).dataize()


class EOerror(EObase, ):
    def dataize(self) -> object:
        raise NotImplementedError()


class EOnumber(EObase, ):
    def __init__(self, value: int | float):
        self.value = value
        self.add = partial(EOnumber_EOadd, self)
        self.sub = partial(EOnumber_EOsub, self)
        self.pow = partial(EOnumber_EOpow, self)
        self.less = partial(EOnumber_EOless, self)
        self.mul = partial(EOnumber_EOmul, self)
        self.leq = partial(EOnumber_EOleq, self)

    def dataize(self):
        return self

    def data(self):
        return self.value

    def __eq__(self, other):
        return EObool("true" if self.value == other.value else "false")

    def __add__(self, other):
        return EOnumber(self.value + other.value)

    def __lt__(self, other):
        return EObool("true" if self.value < other.value else "false")

    def __le__(self, other):
        return self == other or self < other

    def __sub__(self, other):
        return EOnumber(self.value - other.value)

    def __pow__(self, power, modulo=None):
        return EOnumber(self.value ** power.value)

    def __str__(self):
        return f"EOnumber({self.value})"

    def __mul__(self, other):
        return EOnumber(self.value * other.value)


class EObool(EObase, ):
    def __init__(self, value: str):
        self.value = value
        self.If = partial(EObool_EOIf, self)

    def dataize(self):
        return self

    def data(self):
        return bool(self)

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


class EOnumber_EOmul(EOnumber, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() * self.other.dataize()


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


class EOnumber_EOleq(EObool, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__("false")
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() <= self.other.dataize()


class EOnumber_EOpow(EOnumber, ):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() ** self.other.dataize()


class EOarray(EObase):
    def __init__(self, *elements: List[EObase]):
        self.elements = elements
        self.get = partial(EOarray_EOget, self)

    def dataize(self):
        return self

    def data(self):
        return [elem.data() for elem in self.elements]

    def __getitem__(self, item):
        if isinstance(item, EOnumber):
            assert isinstance(item.value, int)
            return self.elements[item.data()]
        else:
            raise AttributeError(f"{item} is not EOnumber!")


class EOarray_EOget(EObase):
    def __init__(self, arr: EOarray, i: EOnumber):
        self.arr = arr
        self.i = i

    def dataize(self):
        return self.arr[self.i]


class EOstring(EObase):
    def __init__(self, value: str):
        self.value = value

    def dataize(self) -> EObase:
        return self

    def data(self):
        return self.value

    def __str__(self):
        return self.value


class EOsprintf(EOstring):
    def __init__(self, fmt: EOstring, *args: EObase):
        super().__init__("ABOBA")
        self.fmt = fmt
        self.args = args

    def dataize(self) -> EObase:
        return EOstring(str(self.fmt) % tuple(arg.dataize().data() for arg in self.args))


class EOstdout(EObase):
    def __init__(self, text: EOstring):
        self.text = text

    def dataize(self) -> EObase:
        print(self.text.dataize())
        return self

    def data(self):
        return None


def lazy_property(fn):
    attr = "_lazy__" + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr):
            value = fn(self)
            setattr(self, attr, value)
        return getattr(self, attr)

    return _lazy_property

