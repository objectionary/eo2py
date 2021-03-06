from eo2py.atoms import *
import pytest
import math


def test_object():
    with pytest.raises(AttributeError) as e:
        Object().dataize()


def test_error():
    with pytest.raises(NotImplementedError) as e:
        DataizationError().dataize()


def test_atom():
    atom = Atom()
    assert atom.dataize() == atom
    with pytest.raises(NotImplementedError):
        Atom().data()


@pytest.mark.parametrize("a", list(range(1, 10)))
@pytest.mark.parametrize("b", list(range(1, 10)))
def test_number(a, b):
    assert Number(a) == Number(Number(a).data())
    assert Number(a) - Number(b) == Number(a).attr_sub()(Number(b)).dataize() == Number(a - b)
    assert Number(a) + Number(b) == Number(a).attr_add()(Number(b)).dataize() == Number(a + b)
    assert Number(a) * Number(b) == Number(a).attr_mul()(Number(b)).dataize() == Number(a * b)
    assert (
            Number(a) ** Number(b)
            == Number(a).attr_pow()(Number(b)).dataize()
            == Number(math.pow(a, b))
    )
    assert (
            (Number(a) < Number(b))
            == Number(a).attr_less()(Number(b)).dataize()
            == Boolean("true" if a < b else "false")
    )
    assert (
            (Number(a) <= Number(b))
            == Number(a).attr_leq()(Number(b)).dataize()
            == Boolean("true" if a <= b else "false")
    )


def test_string():
    value = "String"
    assert (
            str(String(value))
            == str(String(value).dataize())
            == String(value).data()
            == value
    )
    assert not String("12") == Number(12)


def test_array():
    arr = Array()(Number(1))(Number(2))(Number(3))(Number(4))(Number(5))
    for i, number in enumerate(arr):
        assert number.dataize().data() == Attribute(arr, "get")(Number(i)).dataize().data()
    assert arr.dataize() == arr
    assert arr.dataize().data() == arr.data() == [1, 2, 3, 4, 5]
    assert arr[Number(2)] == Number(3)
    with pytest.raises(AttributeError) as e:
        assert arr[2] == Number(3)

    assert Attribute(Array()(Number(2)), "get")(Number(0)).dataize() == Number(2)
    with pytest.raises(IndexError):
        assert Attribute(Array()(Number(2)), "get")(Number(1)).dataize()
    with pytest.raises(ApplicationError):
        assert Attribute(Array()(Number(2)), "get")(Number(1))(Number(2)).dataize()


def test_bool():
    true = Boolean("true")
    false = Boolean("false")
    assert true == Boolean("TRUE") == Boolean("True") == Boolean(" \n True\n")
    assert false == Boolean("FALSE") == Boolean("False") == Boolean("\t\rFalse")
    with pytest.raises(AssertionError) as e:
        false = Boolean("string")
    with pytest.raises(AttributeError) as e:
        false = Boolean(123)
    assert true and not false
    assert str(true) == "Boolean(True)"
    assert str(false) == "Boolean(False)"
    assert Attribute(Boolean(False), "if")(String("true"))(String("false")).dataize() == String("false")
    assert Attribute(Boolean(True), "if")(String("true"))(String("false")).dataize() == String("true")
    with pytest.raises(ApplicationError):
        assert Attribute(Boolean(True), "if")(String("true"))(String("false"))(
            String("something else lmao")).dataize() == String("true")


def test_stdout(capsys):
    stdout = Stdout()(String("Test"))
    assert stdout.data() is None
    stdout.dataize()
    with pytest.raises(ApplicationError):
        Stdout()(String("Test"))("Test2")
    assert capsys.readouterr().out == "Test\n"


def test_lazy_property():
    class A:
        @lazy_property
        def a(self):
            return 12

    obj = A()
    assert hasattr(obj, "a")
    assert obj.a == 12


def attribute_test():
    assert Attribute(Number(2), "add")(Number(2)).dataize() == Number(4)
    assert Attribute(Number(2), "add")(
        Attribute(Number(2), "add")(Number(2))
    ).dataize() == Number(6)
    assert Attribute(
        Attribute(Number(2), "add")(Number(2)), "add"
    )(Number(2)).dataize() == Number(6)
    dx = Number(2)
    dy = Number(2)
    dx_squared = Attribute(dx, "pow")()(Number(2))
    dy_squared = Attribute(dy, "pow")()(Number(2))
    dx_squared_plus_dy_squared = Attribute(dx_squared, "add")(dy_squared)
    sqrt_dx_squared_plus_dy_squared = Attribute(
        dx_squared_plus_dy_squared, "pow"
    )(Number(0.5))
    assert sqrt_dx_squared_plus_dy_squared.dataize() == Number(8 ** 0.5)
