from eo2py.atoms import *
import pytest

"""
[name] > person
"""


class EOperson(ApplicationMixin, Object):
    def __init__(self):
        # Special attributes
        self.attr__phi = DataizationError()
        self.attr__parent = DataizationError()
        self.attr__self = self

        # Free attributes
        self.attributes = ["name"]


def test_person():
    with pytest.raises(ApplicationError) as e:
        assert EOperson()(String("David"))(String("Bowie"))
    with pytest.raises(NotImplementedError) as e:
        assert EOperson()(String("Kate")).dataize()
    assert Attribute(EOperson()(String("Kate")), "name").dataize().data() == "Kate"
