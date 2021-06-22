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
        return EOattr(
            EOattr(
                EOattr(self.dx, 'pow', EOnumber(2)),
                'add',
                EOattr(self.dy, 'pow', EOnumber(2))
            ),
            'pow',
            EOnumber(0.5)
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"vector(dx={self.dx}, dy={self.dy})"


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
        return EOattr(
            vector(
                EOattr(EOattr(self.to, 'x'), 'sub', EOattr(self.__PARENT__, 'x')),
                EOattr(EOattr(self.to, 'x'), 'sub', EOattr(self.__PARENT__, 'x'))
            ),
            'length'
        )

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

    def __str__(self):
        return f"point(x={self.x}, y={self.y})"


class circle_is_inside(EObase):
    def __init__(self, __PARENT__, p):
        self.p = p
        self.__PARENT__ = __PARENT__

    @property
    def __PHI__(self):
        return EOattr(
            EOattr(
                self.__PARENT__,
                'distance',
                self.p
            ),
            'leq',
            EOattr(
                self.__PARENT__,
                'radius'
            )
        )

    def dataize(self) -> EObase:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"{self.__PARENT__}.is_inside(p={self.p})"


class circle(EObase):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def __PHI__(self):
        return self.center

    @property
    def is_inside(self):
        return partial(circle_is_inside, self)

    def dataize(self) -> EObase:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"circle(center={self.center}, radius={self.radius})"


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
        return EOstdout(
            EOsprintf(
                "%s\n",
                EOattr(
                    circle(
                        point(EOnumber(1), EOnumber(1)),
                        EOnumber(2)
                    ),
                    'is_inside',
                    point(EOnumber(22), EOnumber(1))
                )
            )
        )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_vector():
    assert app().dataize()
