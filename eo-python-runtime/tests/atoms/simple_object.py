from eo2py.atoms import *
import pytest

"""
[name] > person
"""


class EOperson(Object):
    def __init__(self, name: Object, ):
        # Special attributes
        self.__PHI__ = DataizationError()
        self.__PARENT__ = DataizationError()
        self.__THIS__ = self

        # Free attributes
        self.name = name

    def dataize(self) -> object:
        return self.__PHI__.dataize()


def test_person():
    with pytest.raises(NotImplementedError) as e:
        assert EOperson(String("Kate")).dataize()
