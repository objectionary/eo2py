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


class EOfibonacci(Object):
    def __init__(self):
        self.__PARENT__ = DataizationError()
        self.__THIS__ = self

        # Free attributes
        self.attributes = ["n"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self


    @property
    def __PHI__(self):
        return Attribute(
            Attribute(self.n, "Less")(Number(2)),
            "If",
        )()(
            self.n)(
            Attribute(
                EOfibonacci()(Attribute(self.n, "Sub")(Number(1))),
                "Add",
            )(EOfibonacci()(Attribute(self.n, "Sub")(Number(2)))),
        )

    def dataize(self):
        return self.__PHI__.dataize()


def test_fibonacci():
    res = EOfibonacci()(Number(10))
    assert res.dataize() == Number(55)
