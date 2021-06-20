from eo2py.atoms import *

"""
[name] > person
"""



class EOperson(EObase):
    def __init__(self, name: EObase, ):
        self.name = name
        self.__PHI__ = EOerror(
            # "The object cannot be dataized because it doesn't contain @ attribute"
        )
        self.__PARENT__ = EOerror(
            # "This is a toplevel object, it has no parents"
        )
        self.__THIS__ = self

    def generate_attributes(self):
        pass

    def dataize(self):
        self.generate_attributes()
        self.__PHI__.dataize()