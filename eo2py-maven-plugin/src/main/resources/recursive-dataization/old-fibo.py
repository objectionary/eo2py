from oldatoms import *


class Fibo(EOInt):
    def __init__(self, n):
        super().__init__("")
        self.n = n

    def dataize(self):
        n = self.n
        self.__PHI__ = EOIf(
            EOLess(n, EOInt("2")),
            n,
            EOAdd(
                Fibo(
                    EOSub(
                        n,
                        EOInt("1")
                    )),
                Fibo(
                    EOSub(
                        n,
                        EOInt("2")
                    ))
            )
        )
        return self.__PHI__.dataize()


if __name__ == "__main__":
    print(Fibo(EOInt("6")).dataize())