from atoms import EOInt, EOIf, EOLess, EOSub, EOAdd, EOError, EOBase

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


class Fibo(EOBase):
    def __init__(self, n: EOBase):
        self.n = n
        self.__PHI__ = EOError("The object cannot be dataized because it doesn't contain @ attribute")
        self.__PARENT__ = EOError("This is a toplevel object, it has no parents")
        self.__THIS__ = self

    def generate_attributes(self):
        self.__PHI__ = EOIf(
            EOLess(self.n, EOInt("2")),
            self.n,
            EOAdd(
                Fibo(
                    EOSub(
                        self.n,
                        EOInt("1")
                    )),
                Fibo(
                    EOSub(
                        self.n,
                        EOInt("2")
                    ))
            )
        )

    def dataize(self):
        self.generate_attributes()
        return self.__PHI__.dataize()


if __name__ == "__main__":
    import sys

    print(sys.version)
    print(Fibo(EOInt("15")).dataize())
