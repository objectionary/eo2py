from eo2py.atoms import *
import pytest

"""
[name] > person
"""


class EOperson(Object):
    def __init__(self):
        # Special attributes
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__THIS__ = self

        # Free attributes
        self.attributes = ["name"]
        self.application_counter = 0

    def __call__(self, arg: Object):
        if self.application_counter >= len(self.attributes):
            raise ApplicationError(arg)
        else:
            setattr(self, self.attributes[self.application_counter], arg)
            self.application_counter += 1
        return self

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_person():
    with pytest.raises(ApplicationError) as e:
        assert EOperson()(String("David"))(String("Bowie"))
    with pytest.raises(NotImplementedError) as e:
        assert EOperson()(String("Kate")).dataize()
    assert Attribute(EOperson()(String("Kate")), "name").dataize()