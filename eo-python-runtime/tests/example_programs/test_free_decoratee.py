from eo2py.atoms import *

"""
[value] > number
  
[@] > decorator
  .add > incremented_value
     value
     1

[args...] > app
  number 5 > n
  decorator n > decorated_number
  stdout > @
    sprintf
      "%d\n"
      decorated_number.value

"""


class EOnumber(ApplicationMixin, Object):

    def __init__(self):

        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["value"]
        self.attr_value = DataizationError()

    def __str__(self):
        return f"number(value={self.attr_value})"


class EOdecorator(ApplicationMixin, Object):

    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["_phi"]
        self.attr__phi = DataizationError()

    @property
    def attr_incremented_value(self):
        return Attribute(Attribute(self, 'value'), 'add')()(Number(1))

    def __str__(self):
        return f"decorator(_phi={self.attr__phi})"


class EOapp(ApplicationMixin, Object):
    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["args"]
        self.varargs = True
        self.attr_args = Array()

    @property
    def attr_n(self):
        # Bound attributes
        return EOnumber()(
            Number(5)
        )

    @property
    def attr_decorated_number(self):
        # Bound attributes
        return EOdecorator()(
            self.attr_n
        )

    @property
    def attr__phi(self):
        return Stdout()(
            Sprintf()(String("%d %d\n"))(
                Attribute(self.attr_decorated_number, 'value')
            )(
                Attribute(self.attr_decorated_number, 'incremented_value')
            )
        )


def test_free_decoratee(capsys):
    assert EOapp().dataize()
    stdout = capsys.readouterr().out.strip()
    assert stdout.splitlines(keepends=True)[-1] == '5 6'
