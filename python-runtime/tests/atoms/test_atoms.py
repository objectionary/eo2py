from eo2py.atoms import *


def test_addition():
    assert EOnumber(2) + EOnumber(3) == EOnumber(2).add(EOnumber(3)).dataize()


if __name__ == "__main__":
    assert EOnumber(2).sub(EOnumber(3)).dataize() == EOnumber(2) - EOnumber(3)
    assert EOnumber(2) ** EOnumber(3) == EOnumber(2).pow(EOnumber(3)).dataize()
    assert EObool("true") == EObool("true")
    assert EOnumber(2) < EOnumber(3)
    assert (EOnumber(2) < EOnumber(3)) == EOnumber(2).less(EOnumber(3)).dataize()

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
