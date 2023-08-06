from typing import Any
from jijmodeling.expression.expression import Operator
import numpy as np


def abs(term):
    return Absolute([term])

def ceil(term):
    return Ceil([term])

def floor(term):
    return Floor([term])

def log(antilog, base=np.e):
    if base not in (2, 10, np.e):
        raise ValueError('log base is 2, 10 or numpy.e') 
    return Log([antilog, base])


class Absolute(Operator):
    def __repr__(self) -> str:
        return '|' + str(self.children[0]) + '|'

    def operation(self, objects: list) -> Any:
        return np.abs(objects[0])


class Ceil(Operator):
    def __repr__(self):
        return '[' + str(self.children[0]) + ']'
    def operation(self, objects: list) -> Any:
        return np.ceil(objects[0])


class Floor(Operator):
    def __repr__(self) -> str:
        return '[' + str(self.children[0]) + ']'
    
    def operation(self, objects: list) -> Any:
        return np.floor(objects[0])


class Log(Operator):

    @property
    def antilog(self):
        return self.children[0]

    @property
    def base(self):
        return self.children[1]

    def __repr__(self) -> str:
        return 'log_{}({})'.format(str(self.base), str(self.antilog))

    def operation(self, objects: list) -> Any:
        if objects[1] == 10:
            return np.log10(objects[0])
        elif self.base == 2:
            return np.log2(objects[0])
        else:
            return np.log(objects[0])