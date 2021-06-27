from eo2py.atoms import *

"""
+package sandbox
+alias sprintf org.eolang.txt.sprintf

[n] > factorial
  if. > @
    less.
      n
      2
    1
    mul.
      n
      factorial
        sub.
          n
          1

[args...] > appFactorial
  sprintf > @
    "%d! = %d\n"
    (args.get 0).toInt > n
    factorial n
    
"""


class EOfactorial(ApplicationMixin, Object):
    def __init__(self):
        self.attr__parent = self
        self.attr__self = self

        # Free attributes
        self.attributes = ["n"]
        self.attr_n = DataizationError()

    @property
    def attr__phi(self):
        return Attribute(
            Attribute(self.attr_n, "less")(Number(2)),
            "if")()(
            Number(1))(
            Attribute(self.attr_n, "mul")()(
                EOfactorial()(Attribute(self.attr_n, "sub")()(Number(1)))
            )
        )


class EOappFactorial(ApplicationMixin, Object):
    def __init__(self):
        self.attributes = ["args"]
        self.attr_args = Array()

    @property
    def n(self):
        return Attribute(self.attr_args, "get")(Number(0))

    @property
    def attr__phi(self):
        return Stdout()\
            (Sprintf()(String("%d! = %d"))(self.n)(EOfactorial()(self.n)))


def test_factorial():
    app = EOfactorial()(Number(5))
    assert app.dataize() == Number(120)
