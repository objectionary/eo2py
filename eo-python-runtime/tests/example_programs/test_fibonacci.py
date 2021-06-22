from eo2py.atoms import *

"""
+package sandbox

[n] > fibonacci
  if. > @
    n.less 2
    n
    add.
      fibonacci (n.sub 1)
      fibonacci (n.sub 2)
"""


# TODO: figure out type resolution
class EOfibonacci(Object):
    def __init__(self, n: Object):
        # super().__init__(0)
        self.n = n
        self.__PARENT__ = DataizationError()
        self.__THIS__ = self

    @property
    def __PHI__(self):
        return Attribute(
            Attribute(self.n, "Less").applied_to(Number(2)),
            "If",
        ).applied_to(
            self.n,
            Attribute(
                EOfibonacci(Attribute(self.n, "Sub").applied_to(Number(1))),
                "Add",
            ).applied_to(EOfibonacci(Attribute(self.n, "Sub").applied_to(Number(2)))),
        )

    def dataize(self):
        return self.__PHI__.dataize()


def test_fibonacci():
    res = EOfibonacci(Number(10))
    assert res.dataize() == Number(55)
