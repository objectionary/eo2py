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


class EOfactorial(Object):
    def __init__(self):
        self.attr__parent = self
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
            "if")()(
            Number(1))(
            Attribute(self.attr_n, "mul")()(
                EOfactorial()(Attribute(self.attr_n, "sub")()(Number(1)))
            )
        )

    def dataize(self) -> object:
        return self.attr__phi.dataize()


class EOappFactorial(Object):
    def __init__(self):
        self.attributes = ["args"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter == 0:
            setattr(self, self.attributes[self.application_counter], [])
            self.application_counter += 1
        getattr(self, self.attributes[0]).append(arg)
        return self

    @property
    def n(self):
        return Attribute(self.args, "get")(Number(0))

    @property
    def attr__phi(self):
        return Stdout()\
            (Sprintf()(String("%d! = %d"))(self.n)(EOfactorial()(self.n)))

    def dataize(self) -> object:
        return self.attr__phi.dataize()


def test_factorial():
    app = EOfactorial()(Number(5))
    assert app.dataize() == Number(120)
