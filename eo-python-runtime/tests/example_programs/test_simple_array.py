from eo2py.atoms import *

"""
[args...] > appArray
  stdout > @
    sprintf
      "%d"
      get.
        *
          5
          2
          4
        0
"""


class EOappArray(Object):
    def __init__(self, *args):
        self.args = args

    @property
    def __PHI__(self):
        return Stdout(
            FormattedString(
                String("%d"), Attribute(Array(*self.args), "Get").applied_to(Number(3))
            )
        )

    def dataize(self):
        return self.__PHI__.dataize()


def test_simple_array():
    app = EOappArray(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
    )
    assert app.dataize()
