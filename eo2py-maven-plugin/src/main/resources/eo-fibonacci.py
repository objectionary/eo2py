import atoms

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


class Fibo(atoms.EOBase):
    def __init__(self, n: atoms.EOBase, ):
        self.n = n
        self.__PHI__ = atoms.EOError("The object cannot be dataized because it doesn't contain @ attribute")
        self.__PARENT__ = atoms.EOError("This is a toplevel object, it has no parents")
        self.__THIS__ = self

    def generate_attributes(self):
        # self.__PHI__ = \
        #     atoms.EOIf(
        #         atoms.EOLess(self.n, atoms.EOInt("2")),
        #         self.n,
        #         atoms.EOAdd(
        #             Fibo(
        #                 atoms.EOSub(
        #                     self.n,
        #                     atoms.EOInt("1")
        #                 )),
        #             Fibo(
        #                 atoms.EOSub(
        #                     self.n,
        #                     atoms.EOInt("2")
        #                 ))
        #         )
        #     )
        # TODO: make constructors lazy
        pass

    def dataize(self):
        self.generate_attributes()
        return self.__PHI__.dataize()


if __name__ == "__main__":
    import sys

    # print(sys.version)
    print(Fibo(atoms.EOInt("15")).dataize())
