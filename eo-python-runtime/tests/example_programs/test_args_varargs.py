from eo2py.atoms import *
import pytest

"""
[arg1, arg2, varargs...] > obj
  stdout > @
    sprintf
      "%d %d %d"
      get.
        varargs
        3
      arg1
      arg2
"""


class EOobj(ApplicationMixin, Object):
    def __init__(self):
        # Free attributes
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["arg1", "arg2", "varargs"]
        self.attr_arg1 = DataizationError()
        self.attr_arg2 = DataizationError()
        self.attr_varargs = Array()
        self.varargs = True

    @property
    def attr__phi(self):
        return Stdout()(
            Sprintf()
            (String("%d %d %d"))
            (self.attr_arg2)
            (Attribute(self.attr_varargs, "get")()(Number(3)))
            (self.attr_arg1)
        )


def test_args_varargs(capsys):
    app1 = EOobj()(Number(-55))(Number(-88))(Number(0))(Number(1))(Number(2))(Number(3))(Number(4))
    assert app1.dataize()
    assert capsys.readouterr().out.splitlines(keepends=True)[-1] == "-88 3 -55\n"
    app2 = EOobj()(Number(-55))(Number(-88))
    with pytest.raises(IndexError) as e:
        assert app2.dataize()
    app3 = EOobj()(Number(-55))
    with pytest.raises(NotImplementedError) as e:
        assert app3.dataize()
