from eo2py.atoms import *

"""
[attr] > a
  attr > a_attr
  
[] > b
  a "something" > @
  
[] > c
  b > @

[] > d
  c > @

[args...] > app
  stdout > @
    sprintf
      "%s\n"
      d.a_attr

"""


class EOa(Object):
    def __init__(self):
        # Special attributes
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self
        # Free attributes
        self.attributes = ["a_attr"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"a(attr={self.a_attr})"


class EOb(Object):
    def __init__(self):
        # Special attributes
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

    @property
    def __PHI__(self):
        return EOa()(String("something"))

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"b()"


class EOc(Object):
    def __init__(self):
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

    @property
    def __PHI__(self):
        return EOb()

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"c()"


class EOd(Object):
    def __init__(self):
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

    @property
    def __PHI__(self):
        return EOc()

    def dataize(self) -> Object:
        return self.__PHI__.dataize()

    def __str__(self):
        return f"d()"


class EOapp(Object):
    def __init__(self, *args, **kwargs):
        # Special attributes
        self.__PARENT__ = DataizationError()
        self.__SELF__ = self

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
            Sprintf()(String("%s\n"))(Attribute(EOd(), 'a_attr')())
            )

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_chained_phi(capsys):
    assert EOapp().dataize()
    stdout = capsys.readouterr().out.strip()
    assert stdout.splitlines(keepends=True)[-1] == 'something'


