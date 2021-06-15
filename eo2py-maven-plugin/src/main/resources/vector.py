from functools import partial
from atoms import *

"""
+package sandbox
+alias stdout org.eolang.io.stdout
+alias sprintf org.eolang.txt.sprintf

[dx dy] > vector
  pow. > length
    add.
      dx.pow 2.0
      dy.pow 2.0
    0.5

[x y] > point
  [to] > distance
    length. > @
      vector
        to.x.sub (^.x)
        to.y.sub (^.y)

[center radius] > circle
  center > @
  [p] > is-inside
    leq. > @
      ^.distance p
      ^.radius

[args...] > app
  stdout > @
    sprintf
      "%f\n"
      distance.
        point 1.0 2.0
        point 4.0 6.0

"""


class vector(EObase):

    def __init__(self, dx, dy):
        # Special attributes
        self.__PHI__ = EOerror()
        self.__PARENT__ = EOerror()
        self.__SELF__ = self

        # Free attributes
        self.dx = dx
        self.dy = dy

    def generate_attributes(self):
        # Bound attributes
        self.length = self.dx.pow(2.0).add(self.dy.pow(2.0)).pow(0.5)

    def dataize(self) -> object:
        self.generate_attributes()
        return self.__PHI__.dataize()


# Inner abstract object
class point_distance(EObase):

    def __init__(self, __PARENT__, to):
        # Special attributes
        self.__PHI__ = EOerror()
        self.__PARENT__ = __PARENT__
        self.__SELF__ = self

        # Free attributes
        self.to = to

    def generate_attributes(self):
        # Bound attributes
        self.__PHI__ = vector(
            self.to.x.sub(self.__PARENT__.x),
            self.to.y.sub(self.__PARENT__.y)
        ).length

    def dataize(self) -> object:
        self.generate_attributes()
        return self.__PHI__.dataize()


# Abstract object is assigned just as attribute
class point(EObase):
    def __init__(self, x, y):
        # Special attributes
        self.__PHI__ = EOerror()
        self.__PARENT__ = EOerror()
        self.__SELF__ = self

        # Free attributes
        self.x = x
        self.y = y

    def generate_attributes(self):
        # Bound attributes
        self.distance = partial(point_distance, self)

    def dataize(self) -> object:
        self.generate_attributes()
        return self.__PHI__.dataize()


class app(EObase):
    def __init__(self, *args):
        # Special attributes
        self.__PHI__ = EOerror()
        self.__PARENT__ = EOerror()
        self.__SELF__ = self

        # Free attributes
        self.args = args

    def generate_attributes(self):
        # Bound attributes
        self.__PHI__ = point(EOnumber(1), EOnumber(2)).distance(
            point(EOnumber(4), EOnumber(6))
        )

    def dataize(self) -> object:
        self.generate_attributes()
        print(self.__PHI__.dataize())
        return None


if __name__ == "__main__":
    app().dataize()