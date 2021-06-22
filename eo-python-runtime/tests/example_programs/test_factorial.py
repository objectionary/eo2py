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
    def __init__(self, n):
        self.n = n
        self.__PARENT__ = self
        self.__THIS__ = self

    @property
    def __PHI__(self):
        return Attribute(
            Attribute(self.n, "Less").applied_to(Number(2)),
            "If",
        ).applied_to(
            Number(1),
            Attribute(self.n, "Mul").applied_to(
                EOfactorial(Attribute(self.n, "Sub").applied_to(Number(1)))
            ),
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


class EOappFactorial(Object):
    def __init__(self, *args):
        self.args = Array(*args)

    @property
    def n(self):
        return Attribute(self.args, "get").applied_to(Number(0))

    @property
    def __PHI__(self):
        return Stdout(FormattedString(String("%d! = %d"), self.n, EOfactorial(self.n)))

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_factorial():
    app = EOfactorial(Number(5))
    assert app.dataize() == Number(120)
