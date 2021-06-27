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


class EOa(ApplicationMixin, Object):
    def __init__(self):
        # Special attributes
        self.attr__parent = DataizationError()
        self.attr__self = self
        # Free attributes
        self.attributes = ["attr"]
        self.attr_attr = DataizationError()

    @property
    def attr_a_attr(self):
        return self.attr_attr

    def __str__(self):
        return f"a(attr={self.attr_a_attr})"


class EOb(ApplicationMixin, Object):
    def __init__(self):
        # Special attributes
        self.attr__parent = DataizationError()
        self.attr__self = self

    @property
    def attr__phi(self):
        return EOa()(String("something"))

    def __str__(self):
        return f"b()"


class EOc(ApplicationMixin, Object):
    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

    @property
    def attr__phi(self):
        return EOb()

    def __str__(self):
        return f"c()"


class EOd(ApplicationMixin, Object):
    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

    @property
    def attr__phi(self):
        return EOc()

    def __str__(self):
        return f"d()"


class EOapp(ApplicationMixin, Object):
    def __init__(self):
        # Special attributes
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["args"]
        self.varargs = True

    @property
    def attr__phi(self):
        # Bound attributes
        return Stdout()(
            Sprintf()(String("%s\n"))(Attribute(EOd(), 'a_attr')())
        )


def test_chained_phi(capsys):
    assert EOapp().dataize()
    stdout = capsys.readouterr().out.strip()
    assert stdout.splitlines(keepends=True)[-1] == 'something'
