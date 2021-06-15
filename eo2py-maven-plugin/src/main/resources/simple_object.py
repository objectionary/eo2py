import atoms

"""
[name] > person
"""



import atoms

class EOperson(atoms.EOBase):
    def __init__(self, name: atoms.EOBase, ):
        self.name = name
        self.__PHI__ = atoms.EOError("The object cannot be dataized because it doesn't contain @ attribute")
        self.__PARENT__ = atoms.EOError("This is a toplevel object, it has no parents")
        self.__THIS__ = self

    def generate_attributes(self):
        pass

    def dataize(self):
        self.generate_attributes()
        self.__PHI__.dataize()