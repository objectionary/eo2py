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
        self.attr__parent = DataizationError()
        self.__THIS__ = self

        # Free attributes
        self.attributes = ["n"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self


    @property
    def attr__phi(self):
        return Attribute(
            Attribute(self.attr_n, "less")(Number(2)),
            "if",
        )()(
            self.attr_n)(
            Attribute(
                EOfibonacci()(Attribute(self.attr_n, "sub")(Number(1))),
                "add",
            )(EOfibonacci()(Attribute(self.attr_n, "sub")(Number(2)))),
        )

    def dataize(self):
        return self.attr__phi.dataize()


def test_fibonacci():
    res = EOfibonacci()(Number(10))
    assert res.dataize() == Number(55)
