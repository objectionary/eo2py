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


class EOnumber(Object):

    def __init__(self):

        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["value"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    def dataize(self) -> object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"number(value={self.attr_value})"


class EOdecorator(Object):

    def __init__(self):
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["_phi"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, "attr_" + self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    @property
    def attr_incremented_value(self):
        return Attribute(Attribute(self, 'value'), 'add')()(Number(1))

    def dataize(self) -> object:
        return self.attr__phi.dataize()

    def __str__(self):
        return f"decorator(_phi={self.attr__phi})"


class EOapp(Object):
    def __init__(self, *args, **kwargs):
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["args"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter == 0:
            setattr(self, self.attributes[self.application_counter], [])
            self.application_counter += 1
        getattr(self, self.attributes[0]).append(arg)
        return self

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

    def dataize(self) -> object:
        return self.attr__phi.dataize()


def test_chained_phi(capsys):
    assert EOapp().dataize()
    stdout = capsys.readouterr().out.strip()
    assert stdout.splitlines(keepends=True)[-1] == '5 6'
