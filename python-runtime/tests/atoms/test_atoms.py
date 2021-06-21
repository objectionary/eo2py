from eo2py.atoms import *
import pytest
import math


def test_base():
    with pytest.raises(NotImplementedError) as e:
        EObase().dataize()


def test_error():
    with pytest.raises(NotImplementedError) as e:
        EOerror().dataize()


@pytest.mark.parametrize("a", list(range(1, 10)))
@pytest.mark.parametrize("b", list(range(1, 10)))
def test_number(a, b):
    assert EOnumber(a) == EOnumber(EOnumber(a).data())
    assert EOnumber(a) - EOnumber(b) == EOnumber(a).sub(EOnumber(b)).dataize() == EOnumber(a - b)
    assert EOnumber(a) + EOnumber(b) == EOnumber(a).add(EOnumber(b)).dataize() == EOnumber(a + b)
    assert EOnumber(a) * EOnumber(b) == EOnumber(a).mul(EOnumber(b)).dataize() == EOnumber(a * b)
    assert EOnumber(a) ** EOnumber(b) == EOnumber(a).pow(EOnumber(b)).dataize() == EOnumber(math.pow(a, b))
    assert (EOnumber(a) < EOnumber(b)) == EOnumber(a).less(EOnumber(b)).dataize() == \
           EObool("true" if a < b else "false")
    assert (EOnumber(a) <= EOnumber(b)) == EOnumber(a).leq(EOnumber(b)).dataize() == \
           EObool("true" if a <= b else "false")


def test_string():
    value = "String"
    assert str(EOstring(value)) == str(EOstring(value).dataize()) == EOstring(value).data() == value


def test_array():
    arr = EOarray(EOnumber(1), EOnumber(2), EOnumber(3), EOnumber(4), EOnumber(5))
    assert arr.dataize() == arr
    assert arr.dataize().data() == arr.data() == [1, 2, 3, 4, 5]
    assert arr[EOnumber(2)] == EOnumber(3)
    with pytest.raises(AttributeError) as e:
        assert arr[2] == EOnumber(3)


def test_bool():
    true = EObool("true")
    false = EObool("false")
    assert true == EObool("TRUE") == EObool("True") == EObool(" \n True\n")
    assert false == EObool("FALSE") == EObool("False") == EObool("\t\rFalse")
    with pytest.raises(AssertionError) as e:
        false = EObool("string")
    assert true and not false
    assert str(true) == "EObool(True)"
    assert str(false) == "EObool(False)"


def test_stdout(capsys):
    stdout = EOstdout(EOstring("Test"))
    assert stdout.data() is None
    stdout.dataize()
    assert capsys.readouterr().out == "Test\n"




def test_lazy_property():
    class A:
        @lazy_property
        def a(self):
            return 12

    obj = A()
    assert hasattr(obj, 'a')
    assert obj.a == 12


if __name__ == "__main__":
    assert EOattr(EOnumber(2), 'add', EOnumber(2)).dataize() == EOnumber(4)
    assert EOattr(EOnumber(2), 'add', EOattr(EOnumber(2), 'add', EOnumber(2))).dataize() == EOnumber(6)
    assert EOattr(EOattr(EOnumber(2), 'add', EOnumber(2)), 'add', EOnumber(2)).dataize() == EOnumber(6)
    dx = EOnumber(2)
    dy = EOnumber(2)
    dx_squared = EOattr(dx, 'pow', EOnumber(2))
    dy_squared = EOattr(dy, 'pow', EOnumber(2))
    dx_squared_plus_dy_squared = EOattr(dx_squared, 'add', dy_squared)
    sqrt_dx_squared_plus_dy_squared = EOattr(dx_squared_plus_dy_squared, 'pow', EOnumber(0.5))
    assert sqrt_dx_squared_plus_dy_squared.dataize() == EOnumber(8 ** 0.5)
