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


class EOfibonacci(ApplicationMixin, Object):
    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

        # Free attributes
        self.attributes = ["n"]
        self.attr_n = DataizationError()

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


def test_fibonacci():
    res = EOfibonacci()(Number(10))
    assert res.dataize() == Number(55)
