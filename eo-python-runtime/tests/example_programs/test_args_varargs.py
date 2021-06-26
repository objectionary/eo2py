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


class EOobj(Object):
    def __init__(self):
        # Free attributes
        self.attributes = ["arg1", "arg2", "varargs"]
        self.attr_varargs = Array()
        self.application_counter = 0
        self.varargs = True

    def __call__(self, arg: Object):
        if not self.varargs:
            if self.application_counter >= len(self.attributes):
                raise ApplicationError(arg)
            else:
                setattr(self, "attr_" + self.attributes[self.application_counter], arg)
                self.application_counter += 1
        else:
            if self.application_counter < len(self.attributes) - 1:
                setattr(self, "attr_" + self.attributes[self.application_counter], arg)
                self.application_counter += 1
            elif self.application_counter == len(self.attributes) - 1:
                getattr(self, "attr_" + self.attributes[self.application_counter])(arg)
        return self

    @property
    def attr__phi(self):
        return Stdout()(
            Sprintf()
            (String("%d %d %d"))
            (self.attr_arg2)
            (Attribute(self.attr_varargs, "get")()(Number(3)))
            (self.attr_arg1)
        )

    def dataize(self):
        return self.attr__phi.dataize()


def test_args_varargs(capsys):
    app1 = EOobj()(Number(-55))(Number(-88))(Number(0))(Number(1))(Number(2))(Number(3))(Number(4))
    assert app1.dataize()
    assert capsys.readouterr().out.splitlines(keepends=True)[-1] == "-88 3 -55\n"
    app2 = EOobj()(Number(-55))(Number(-88))
    with pytest.raises(IndexError) as e:
        assert app2.dataize()
    app3 = EOobj()(Number(-55))
    with pytest.raises(AttributeError) as e:
        assert app3.dataize()
