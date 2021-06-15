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
        self.add = partial(EOint_EOadd, self)

    def dataize(self) -> int:
        return self.value


class EOint_EOadd(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() + self.other.dataize()


class EOint_EOpow(EOnumber):
    def __init__(self, parent: EOnumber, other: EOnumber):
        super().__init__(0)
        self.parent = parent
        self.other = other

    def dataize(self):
        return self.parent.dataize() ^ self.other.dataize()


if __name__ == "__main__":
    print(EOnumber(2).add(EOnumber(3)).dataize())
