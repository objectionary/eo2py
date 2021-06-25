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
    def __init__(self):
        # Special attributes
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.attributes = ["dx", "dy"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def length(self):
        # Bound attributes
        return Attribute(
            Attribute(
                Attribute(self.dx, "Pow")(Number(2)),
                "Add",
            )(Attribute(self.dy, "Pow")(Number(2))),
            "Pow",
        )(Number(0.5))

    def dataize(self) -> object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"vector(dx={self.dx}, dy={self.dy})"


# Inner abstract object
class EOpoint_distance(Object):
    def __init__(self, __PARENT__):
        # Special attributes
        super().__init__()
        self.__PARENT__ = __PARENT__
        self.__SELF__ = self

        # Free attributes
        self.attributes = ["to"]
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
        # Bound attributes
        return Attribute(
            EOvector()
                (Attribute(Attribute(self.to, "x"), "Sub")(
                    Attribute(self.__PARENT__, "x")))
                (Attribute(Attribute(self.to, "y"), "Sub")(
                    Attribute(self.__PARENT__, "y"))),
            "length"
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


# Abstract object is assigned just as attribute
class EOpoint(Object):
    def __init__(self):
        # Special attributes
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.attributes = ["x", "y"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def distance(self):
        return partial(EOpoint_distance, self)

    def dataize(self) -> object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"point(x={self.x}, y={self.y})"


class EOcircle_is_inside(Object):

    def __init__(self, __PARENT__):
        self.__PARENT__ = __PARENT__
        # Free attributes
        self.attributes = ["p"]
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
            Attribute(self.__PARENT__, "distance")(self.p), "Leq"
        )(Attribute(self.__PARENT__, "radius"))

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"{self.__PARENT__}.is_inside(p={self.p})"


class EOcircle(Object):
    def __init__(self):
        # Free attributes
        self.attributes = ["center", "radius"]
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
        return self.center

    @property
    def is_inside(self):
        return partial(EOcircle_is_inside, self)

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"circle(center={self.center}, radius={self.radius})"


class EOapp(Object):
    def __init__(self):
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

        # Free attributes
        self.attributes = ["args"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter == 0:
            setattr(self, self.attributes[self.application_counter], [])
            self.application_counter += 1
        getattr(self, self.attributes[0]).append(arg)
        return self

    @property
    def __PHI__(self):
        # Bound attributes
        return Stdout()(
            Sprintf()
                (String("%s\n"))
                (Attribute(
                    EOcircle()(EOpoint()(Number(1))(Number(1)))(Number(2)), "is_inside"
                )(EOpoint()(Number(22))(Number(1))))
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_vector():
    assert EOvector()(Number(1))(Number(1))
    assert EOapp().dataize()
