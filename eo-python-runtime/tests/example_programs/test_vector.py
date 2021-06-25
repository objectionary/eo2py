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
        self.attr__parent = DataizationError()
        self.attr__self = self

        # Free attributes
        self.attributes = ["dx", "dy"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr_length(self):
        # Bound attributes
        return Attribute(
            Attribute(
                Attribute(self.attr_dx, "pow")(Number(2)),
                "add",
            )(Attribute(self.attr_dy, "pow")(Number(2))),
            "pow",
        )(Number(0.5))

    def dataize(self) -> object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"vector(dx={self.attr_dx}, dy={self.attr_dy})"


# Inner abstract object
class EOpoint_distance(Object):
    def __init__(self, attr__parent):
        # Special attributes
        super().__init__()
        self.attr__parent = attr__parent
        self.attr__self = self

        # Free attributes
        self.attributes = ["to"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr__phi(self):
        # Bound attributes
        return Attribute(
            EOvector()
                (Attribute(Attribute(self.attr_to, "x"), "sub")(
                    Attribute(self.attr__parent, "x")))
                (Attribute(Attribute(self.attr_to, "y"), "sub")(
                    Attribute(self.attr__parent, "y"))),
            "length"
        )

    def dataize(self) -> object:
        return self.attr__phi.dataize()


# Abstract object is assigned just as attribute
class EOpoint(Object):
    def __init__(self):
        # Special attributes
        # self.attr__phi = DataizationError()
        self.attr__parent = DataizationError()
        self.attr__self = self

        # Free attributes
        self.attributes = ["x", "y"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr_distance(self):
        return partial(EOpoint_distance, self)

    def dataize(self) -> object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"point(x={self.attr_x}, y={self.attr_y})"


class EOcircle_is_inside(Object):

    def __init__(self, attr__parent):
        self.attr__parent = attr__parent
        # Free attributes
        self.attributes = ["p"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr__phi(self):
        return Attribute(
            Attribute(self.attr__parent, "distance")(self.attr_p), "leq"
        )(Attribute(self.attr__parent, "radius"))

    def dataize(self) -> Object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"{self.attr__parent}.is_inside(p={self.attr_p})"


class EOcircle(Object):
    def __init__(self):
        # Free attributes
        self.attributes = ["center", "radius"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr__phi(self):
        return self.attr_center

    @property
    def attr_is_inside(self):
        return partial(EOcircle_is_inside, self)

    def dataize(self) -> Object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"circle(center={self.attr_center}, radius={self.attr_radius})"


class EOapp(Object):
    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

        # Free attributes
        self.attributes = ["args"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter == 0:
            setattr(self, "attr_" + self.attributes[self.application_counter], [])
            self.application_counter += 1
        getattr(self, "attr_" + self.attributes[0]).append(arg)
        return self

    @property
    def attr__phi(self):
        # Bound attributes
        return Stdout()(
            Sprintf()
                (String("%s\n"))
                (Attribute(
                    EOcircle()(EOpoint()(Number(1))(Number(1)))(Number(2)), "is_inside"
                )(EOpoint()(Number(22))(Number(1))))
        )

    def dataize(self) -> object:
        return self.attr__phi.dataize()


def test_vector():
    assert EOvector()(Number(1))(Number(1))
    assert EOapp().dataize()
