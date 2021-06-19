from atoms import *

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


class factorial(EObase):
    def __init__(self, n):
        self.n = n
        self.__PARENT__ = self
        self.__THIS__ = self

    @property
    def __PHI__(self):
        return EOattr(
            EOattr(self.n, 'less', EOnumber(2)),
            'If',
            EOnumber(1),
            EOattr(self.n,
                   'mul',
                   factorial(
                       EOattr(self.n, 'sub', EOnumber(1))
                   )
                   )
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


class appFactorial(EObase):
    def __init__(self, *args):
        self.args = EOarray(*args)

    @property
    def n(self):
        return EOattr(self.args, 'get', EOnumber(0))

    @property
    def __PHI__(self):
        return EOstdout(
            EOsprintf(
                EOstring("%d! = %d"),
                self.n,
                factorial(self.n)
            )
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


if __name__ == "__main__":
    app = appFactorial(EOnumber(10))
    app.dataize()
