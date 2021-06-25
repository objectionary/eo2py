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
        self.__PARENT__ = self
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
            "If")()(
            Number(1))(
            Attribute(self.n, "Mul")()(
                EOfactorial()(Attribute(self.n, "Sub")()(Number(1)))
            )
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


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
    def __PHI__(self):
        return Stdout()\
            (Sprintf()(String("%d! = %d"))(self.n)(EOfactorial()(self.n)))

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_factorial():
    app = EOfactorial()(Number(5))
    assert app.dataize() == Number(120)
