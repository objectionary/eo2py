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

    @property
    def length(self):
        # Bound attributes
        return self.dx.pow(EOnumber(2)).add(self.dy.pow(EOnumber(2))).pow(EOnumber(0.5))

    def dataize(self) -> object:
        return self.__PHI__.dataize()


# Inner abstract object
class point_distance(EObase):

    def __init__(self, __PARENT__, to):
        # Special attributes
        super().__init__()
        self.__PARENT__ = __PARENT__
        self.__SELF__ = self

        # Free attributes
        self.to = to

    @property
    def __PHI__(self):
        # Bound attributes
        return vector(
            self.to.x.sub(self.__PARENT__.x),
            self.to.y.sub(self.__PARENT__.y)
        ).length

    def dataize(self) -> object:
        return self.__PHI__.dataize()


# Abstract object is assigned just as attribute
class point(EObase):
    def __init__(self, x, y):
        # Special attributes
        super().__init__()
        self.__PHI__ = EOerror()
        self.__PARENT__ = EOerror()
        self.__SELF__ = self

        # Free attributes
        self.x = x
        self.y = y

    @property
    def distance(self):
        # Bound attributes
        return partial(point_distance, self)

    def dataize(self) -> object:
        return self.__PHI__.dataize()


class app(EObase):
    def __init__(self, *args, **kwargs):
        # Special attributes
        super().__init__()
        self.__PARENT__ = EOerror()
        self.__SELF__ = self

        # Free attributes
        self.args = args

    @property
    def __PHI__(self):
        # Bound attributes
        return point(EOnumber(1), EOnumber(2)).distance(
            point(EOnumber(4), EOnumber(6))
        )

    def dataize(self) -> object:
        print(self.__PHI__.dataize())
        return None


if __name__ == "__main__":
    app().dataize()