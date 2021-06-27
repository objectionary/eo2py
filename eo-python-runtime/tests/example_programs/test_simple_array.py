from eo2py.atoms import *

"""
[args...] > appArray
  stdout > @
    sprintf
      "%d"
      get.
        args
        3
"""


class EOappArray(ApplicationMixin, Object):
    def __init__(self):
        # Free attributes
        self.attributes = ["args"]
        self.attr_args = Array()
        self.varargs = True

    @property
    def attr__phi(self):
        return Stdout()(
                Sprintf()
                (String("%d"))
                (Attribute(
                    self.attr_args,
                    "get")()(Number(3)))
                )


def test_simple_array():
    app = EOappArray()(Number(1))(Number(2))(Number(3))(Number(4))(Number(5))
    assert app.dataize()
