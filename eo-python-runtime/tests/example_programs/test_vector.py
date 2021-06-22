from eo2py.atoms import *

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
      "%b\n"
      is-inside.
        circle
          point 1.0 1.0
          2.0
        point 1.0 1.0

"""


class EOvector(Object):
    def __init__(self, dx, dy):
        # Special attributes
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.dx = dx
        self.dy = dy

    @property
    def length(self):
        # Bound attributes
        return Attribute(
            Attribute(
                Attribute(self.dx, "Pow").applied_to(Number(2)),
                "Add",
            ).applied_to(Attribute(self.dy, "Pow").applied_to(Number(2))),
            "Pow",
        ).applied_to(Number(0.5))

    def dataize(self) -> object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"vector(dx={self.dx}, dy={self.dy})"


# Inner abstract object
class EOpoint_distance(Object):
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
        return Attribute(
            EOvector(
                Attribute(Attribute(self.to, "x"), "Sub").applied_to(
                    Attribute(self.__PARENT__, "x")
                ),
                Attribute(Attribute(self.to, "x"), "Sub").applied_to(
                    Attribute(self.__PARENT__, "x")
                ),
            ),
            "length",
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


# Abstract object is assigned just as attribute
class EOpoint(Object):
    def __init__(self, x, y):
        # Special attributes
        super().__init__()
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.x = x
        self.y = y

    @property
    def distance(self):
        # Bound attributes
        return partial(EOpoint_distance, self)

    def dataize(self) -> object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"point(x={self.x}, y={self.y})"


class EOcircle_is_inside(Object):
    def __init__(self, __PARENT__, p):
        self.p = p
        self.__PARENT__ = __PARENT__

    @property
    def __PHI__(self):
        return Attribute(
            Attribute(self.__PARENT__, "distance").applied_to(self.p), "Leq"
        ).applied_to(Attribute(self.__PARENT__, "radius"))

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"{self.__PARENT__}.is_inside(p={self.p})"


class EOcircle(Object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def __PHI__(self):
        return self.center

    @property
    def is_inside(self):
        return partial(EOcircle_is_inside, self)

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"circle(center={self.center}, radius={self.radius})"


class EOapp(Object):
    def __init__(self, *args, **kwargs):
        # Special attributes
        super().__init__()
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.args = args

    @property
    def __PHI__(self):
        # Bound attributes
        return Stdout(
            FormattedString(
                String("%s\n"),
                Attribute(
                    EOcircle(EOpoint(Number(1), Number(1)), Number(2)), "is_inside"
                ).applied_to(EOpoint(Number(22), Number(1))),
            )
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_vector():
    assert EOapp().dataize()
