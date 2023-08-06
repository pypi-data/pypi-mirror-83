from abc import ABCMeta, abstractmethod
from typing import Any
import inspect
import numpy as np
from jijmodeling.expression.from_serializable import from_serializable, _cls_serializable_validation

class Expression(metaclass=ABCMeta):
    """All component inheritance this class.
    This class provide computation rules and each component.
    """

    remove_element = []

    def __init__(self, children: list):
        self.children = [c for c in children if c not in self.remove_element]
        # Collect the un-summarized indices of each child.
        self.index_labels = []
        for child in self.children:
            if isinstance(child, Expression):
                self.index_labels += child.index_labels
        self.index_labels = list(set(self.index_labels))

    def __add__(self, other):
        # TODO: check type of other
        return Add([self, other])

    def __radd__(self, other):
        return self.__add__(other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __rsub__(self, other):
        return Add([other, -1*self])

    def __lsub__(self, other):
        return Add([self, -1*other])

    def __mul__(self, other):
        return Mul([self, other])
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __lmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Div([self, other])

    def __rtruediv__(self, other):
        return Div([other, self])

    def __pow__(self, other):
        return Power([self, other])

    def __rpow__(self, other):
        return Power([other, self])

    def __mod__(self, other):
        return Mod([self, other])


    def to_serializable(self):

        def express_to_ser(s):
            if 'to_serializable' in dir(s):
                return s.to_serializable()
            elif isinstance(s, (list, tuple)):
                return {
                    'iteratable': 'list' if isinstance(s, list) else 'tuple',
                    'value': [express_to_ser(t) for t in s],
                }
            elif isinstance(s, dict):
                return {k: express_to_ser(v) for k,v in s.items()}
            else:
                return s
        serializable = {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {k: express_to_ser(v) for k, v in vars(self).items()}
        }
        return serializable

    def to_pyqubo(self, placeholder={}, fixed_variables={}, index_values={}):
        # type check
        _ph = {k: np.array(v) if isinstance(v, list) else v for k, v in placeholder.items()}
        from jijmodeling.transpilers.to_pyqubo import to_pyqubo
        return to_pyqubo(self, placeholder=_ph, fixed_variables=fixed_variables, index_values=index_values)

    @classmethod
    def from_serializable(cls, serializable: dict):
        _cls_serializable_validation(serializable, cls)
        init_args = inspect.getfullargspec(cls.__init__).args
        init_args_values = {arg: from_serializable(serializable['attributes'][arg]) for arg in init_args if arg != 'self'}
        return cls(**init_args_values)

class Operator(Expression, metaclass=ABCMeta):
    @abstractmethod
    def operation(self, objects:list)->Any:
        pass
        

class Add(Operator):

    remove_element = [0]

    def __add__(self, other):
        if isinstance(other, Add):
            self.children += other.children
        else:
            self.children.append(other)
        return self

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            str_repr += t.__repr__() + ' + '
        return str_repr[:-3]

    def operation(self, objects:list):
        return sum(objects)


class Mul(Operator):
    def __mul__(self, other):
        if isinstance(other, Mul):
            self.children += other.children
        else:
            self.children.append(other)
        return self

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Add) and len(t.children) > 1:
                str_repr += '({})'.format(t.__repr__())
            elif isinstance(t, (int, float)):
                str_repr += '({})'.format(t.__repr__())
            else:
                str_repr += t.__repr__()
        return str_repr

    def operation(self, objects: list):
        term = 1
        for obj in objects:
            term *= obj
        return term

class Div(Operator):
    def __init__(self, children: list):
        # TODO: raise error when divide zero
        # self.children = [numerator, denominator]
        super().__init__(children)

    def __repr__(self):
        str_repr = ""
        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '(%s)' % t.__repr__()
            if isinstance(t, (int, float)):
                return '({})'.format(t.__repr__())
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '/' + get_str(self.children[1])
        return str_repr

    def operation(self, objects):
        return objects[0]/objects[1]

class Power(Operator):
    @property
    def base(self):
        return self.children[0]

    @property
    def exponent(self):
        return self.children[1]

    def operation(self, objects: list):
        return objects[0]**objects[1] 

    def __repr__(self) -> str:
        return str(self.base) + '^' + str(self.exponent)


class Mod(Operator):
    def __repr__(self):
        str_repr = ""
        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '(%s)' % t.__repr__()
            if isinstance(t, (int, float)):
                return '({})'.format(t.__repr__())
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '%' + get_str(self.children[1])
        return str_repr
    def operation(self, objects: list) -> Any:
        return objects[0]%objects[1]



class Ceil(Operator):
    def __repr__(self):
        return '[' + str(self.children[0]) + ']'
    def operation(self, objects: list) -> Any:
        return int(objects[0]) + 1


class Log(Operator):

    def __init__(self, antilog, base=None) -> None:
        super().__init__([antilog, base])

        self.antilog = antilog
        self.base = base

    def __repr__(self) -> str:
        return 'log_{}({})'.format(str(self.base), str(self.antilog))

    def operation(self, objects: list) -> Any:
        if objects[1] == 10:
            return np.log10(objects[0])
        elif self.base == 2:
            return np.log2(objects[0])
        else:
            return np.log(objects[0])