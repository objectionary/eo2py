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


class appArray(EObase):
    def __init__(self, *args):
        self.args = args

    @property
    def __PHI__(self):
        return EOstdout(
            EOsprintf(
                EOstring("%d"),
                EOattr(
                    EOarray(*self.args),
                    'get',
                    EOnumber(3)
                )
            )
        )

    def dataize(self):
        return self.__PHI__.dataize()


def test_simple_array():
    app = appArray(
        EOnumber(1),
        EOnumber(2),
        EOnumber(3),
        EOnumber(4),
        EOnumber(5),
    )
    assert app.dataize()
