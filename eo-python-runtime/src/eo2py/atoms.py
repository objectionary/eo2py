from abc import abstractmethod
from functools import partial, reduce
from typing import List, Union, Optional, Callable
import operator


class ApplicationMixin:
    varargs: bool = False
    application_counter: int = 0
    attributes: List[str] = []

    def __call__(self, *args: "Object"):
        if len(args) == 1:
            arg = args[0]
            if not self.varargs:
                if self.application_counter >= len(self.attributes):
                    raise ApplicationError(arg)
                else:
                    setattr(self, "attr_" + self.attributes[self.application_counter], arg)
                    self.application_counter += 1
            else:
                if self.application_counter < len(self.attributes) - 1:
                    setattr(self, "attr_" + self.attributes[self.application_counter], arg)
                    self.application_counter += 1
                elif self.application_counter == len(self.attributes) - 1:
                    getattr(self, "attr_" + self.attributes[self.application_counter])(arg)
        return self


class Object:
    attr__phi: "Object"

    def dataize(self) -> "Atom":
        return self.attr__phi.dataize()


class Atom(Object):
    def dataize(self) -> "Atom":
        return self

    @abstractmethod
    def data(self) -> object:
        raise NotImplementedError()


class Attribute(Object):
    def __init__(self, obj: Object, name: str):
        self.obj = obj
        self.name = name
        self.args: List[Object] = []

    def __call__(self, *args: Object):
        self.args.extend(args)
        return self

    def inner_name(self):
        return "attr_" + self.name

    def __str__(self):
        return f"{self.obj}.{self.inner_name()}"

    def dataize(self) -> Atom:
        attr: Optional[Object]
        if hasattr(self.obj, self.inner_name()):
            print(f"Found .{self.inner_name()} in {self.obj}.")
            attr = getattr(self.obj, self.inner_name())
        elif hasattr(self.obj, "attr__phi"):
            print(
                f"Did not find .{self.inner_name()} in {self.obj}, searching for .{self.inner_name()} in {self.obj}'s "
                f"phi attribute: {self.obj.attr__phi}."
            )
            attr = Attribute(self.obj.attr__phi, self.name)
        else:
            print(f"Attribute .{self.inner_name()} was not found.")
            attr = None

        if attr is not None:
            if callable(attr):
                print(f"Dataizing {attr} applied to {[str(arg) for arg in self.args]}.")
                res = reduce(lambda obj, arg: obj(arg), self.args, attr())
                return res.dataize()
            else:
                print(f"Dataizing {attr}, no args needed.")
                return attr.dataize()

        print(f"Dataizing {self.obj}...")
        attr = getattr(self.obj.dataize(), self.inner_name())()
        attr = reduce(lambda obj, arg: obj(arg), self.args, attr)
        return attr.dataize()


class DataizationError(Object):
    def dataize(self) -> None:
        raise NotImplementedError()


class ApplicationError(Exception):
    def __init__(self, arg):
        super().__init__(f"Object cannot be copied with {arg} as argument")


class Number(Atom):
    def __init__(self, value: Union[int, float]):
        self.value = value
        self.attr_add = partial(NumberOperation, self, operator.add)
        self.attr_sub = partial(NumberOperation, self, operator.sub)
        self.attr_pow = partial(NumberOperation, self, operator.pow)
        self.attr_less = partial(NumberOperation, self, operator.lt)
        self.attr_mul = partial(NumberOperation, self, operator.mul)
        self.attr_leq = partial(NumberOperation, self, operator.le)
        self.attr_eq = partial(NumberOperation, self, operator.eq)

    def data(self) -> Union[int, float]:
        return self.value

    def __eq__(self, other) -> "Boolean":
        return Boolean("true" if self.data() == other.data() else "false")

    def __add__(self, other) -> "Number":
        return Number(self.value + other.value)

    def __lt__(self, other) -> "Boolean":
        return Boolean("true" if self.data() < other.data() else "false")

    def __le__(self, other) -> "Boolean":
        return self == other or self < other

    def __sub__(self, other) -> "Number":
        return Number(self.value - other.value)

    def __mul__(self, other) -> "Number":
        return Number(self.value * other.value)

    def __pow__(self, power, modulo=None) -> "Number":
        return Number(self.value ** power.value)

    def __str__(self):
        return f"Number({self.value})"


class Boolean(Atom):
    def __init__(self, value: Union[str, bool]):
        self.value: bool
        if isinstance(value, str):
            value = value.lower().strip()
            assert value == "true" or value == "false"
            self.value = value == "true"
        elif isinstance(value, bool):
            self.value = value
        else:
            raise AttributeError("Boolean: value should be either str or bool")

        self.attr_if = partial(BooleanIf, self)

    def data(self) -> bool:
        return self.value

    def __bool__(self):
        return self.data()

    def __str__(self):
        return f"Boolean({bool(self)})"

    def __eq__(self, other):
        return Boolean(bool(self) == bool(self))


class NumberOperation(ApplicationMixin, Object):
    def __init__(self, parent: Number, operation: Callable[[Atom, Atom], Atom]):
        self.operation = operation
        self.parent = parent

        self.attributes = ["other", ]
        self.attr_other: Optional[Object] = DataizationError()

    def dataize(self) -> Atom:
        return self.operation(self.parent.dataize(), self.attr_other.dataize())


class BooleanIf(ApplicationMixin, Object):
    def __init__(self, parent: Boolean):
        self.parent = parent

        self.attributes = ["if_true", "if_false"]
        self.application_counter = 0
        self.attr_if_true: Optional[Object] = DataizationError()
        self.attr_if_false: Optional[Object] = DataizationError()

    def dataize(self) -> Atom:
        return (
            self.attr_if_true.dataize() if self.parent.dataize() else self.attr_if_false.dataize()
        )


class Array(Atom):
    def __init__(self):
        self.elements = []
        self.attr_get = partial(ArrayGet, self)

    def __call__(self, arg: Object):
        self.elements.append(arg)
        return self

    def __iter__(self):
        return self.elements.__iter__()

    def data(self) -> List:
        return [elem.dataize().data() for elem in self.elements]

    def __getitem__(self, item: Object):
        if isinstance(item, Object):
            index = item.dataize().data()
            assert isinstance(index, int)
            return self.elements[index]
        else:
            raise AttributeError(f"{item} is not a subtype of Object!")


class ArrayGet(ApplicationMixin, Object):
    def __init__(self, arr):
        self.arr = arr

        self.attributes = ["i"]
        self.attr_i = DataizationError()

    def dataize(self) -> Atom:
        return self.arr[self.attr_i].dataize()


class String(Atom):
    def __init__(self, value: str):
        self.value = value

    def data(self) -> str:
        return self.value

    def __eq__(self, other):
        if isinstance(other, String):
            return Boolean(self.value == other.value)
        return Boolean(False)

    def __str__(self):
        return self.value


class Sprintf(ApplicationMixin, Object):
    def __init__(self):
        self.attributes = ["fmt", "args"]
        self.attr_fmt = DataizationError()
        self.attr_args = Array()
        self.varargs = True

    def dataize(self) -> Object:
        return String(str(self.attr_fmt) % tuple(arg.dataize().data() for arg in self.attr_args))


class Stdout(ApplicationMixin, Atom):
    def __init__(self):
        # Free attributes
        self.attributes = ["text"]
        self.attr_text = DataizationError()

    def dataize(self) -> Object:
        print(self.attr_text.dataize())
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
