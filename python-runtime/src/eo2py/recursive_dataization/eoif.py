# from atoms import *
# import function_pattern_matching as fpm
#
# from lazy import lazy
# from src.eo2py.atoms import EObase
#
#
# class EObool(EObase):
#     def __init__(self, value: bool):
#         self.value = value
#         # self.if = partial(EOint_EOadd, self)
#
#     def dataize(self) -> bool:
#         return self.value
#
# # as per PEP 622
# class EObool_if(EObase):
#     def __init__(self, args):
#         match args:
#             case EOTrue, X, _:
#                 self.__dict__.update(X.__dict__)
#             case EOFalse, _, X:
#                 self.__dict__.update(X.__dict__)
#
#
#
#
# class EObool_if(EObase):
#     def __init__(self, condition: EObool, iftrue: EObase, iffalse: EObase):
#         self.condition = condition
#         self.iftrue = iftrue
#         self.iffalse = iffalse
#
#     def dataize(self) -> object:
#         return self.iftrue.dataize() if self.dataize() else self.iffalse.dataize()
#
#
