from typing import Union
from jijmodeling.expression.expression import Expression, _latex_repr
from jijmodeling.variables.variable import Placeholder, Variable
from jijmodeling.expression.sum import Sum

class Tensor(Variable):
    def __init__(self, label, variable, shape, index_labels):
        super().__init__(label)
        self.variable = variable
        self.shape = (shape, ) if isinstance(shape, int) else shape
        self.index_labels = index_labels

    def _rdiv_validate(self, other):
        self.variable._rdiv_validate(other)

    def __repr__(self):
        index_str = ''
        for i in self.index_labels:
            index_str += '[%s]' % i
        return self.label + index_str

    def __make_latex__(self):
        t_str = self.label
        t_str += "_{{{}}}".format(','.join([_latex_repr(ind, False) for ind in self.index_labels]))
        return t_str


class ArraySizePlaceholder(Placeholder):
    def __init__(self, label:str, array_label: str, dimension: int):
        super().__init__(label)
        self.array_label = array_label
        self.dimension = dimension

    def __make_latex__(self):
        return "|" + self.array_label + "|_" + "{{{}}}".format(self.dimension + 1)


class Array:
    def __init__(self, variable: Variable, shape):
        self.variable: Variable = variable
        self.var_label: str = variable.label
        self._shape = shape if isinstance(shape, tuple) else (shape, )
        self.dim: int = len(self._shape)

    @property
    def shape(self):
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                array_size = ArraySizePlaceholder(
                                label=self.var_label + '_shape_%d' % i, 
                                array_label=self.var_label,
                                dimension=i
                            )
                shape.append(array_size)
            else:
                shape.append(s)
        return tuple(shape)

    def __getitem__(self, key)->Union[Tensor, Sum]:
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.var_label, self.dim))

        indices = []
        summation_index = []
        for i, k in enumerate(list(key)):
            # for syntaxsugar x[:]
            # If a slice [:] is used for a key, 
            # it is syntax-sugar that represents Sum, 
            # and the index is automatically created and assigned.
            # i.e. x[:] => Sum({':x_0': n}, x[':x_0']) 
            # This created index is stored in summation_index as Sum will be added later.
            if isinstance(k, slice):
                indices.append(':{}_{}'.format(self.var_label, i))
                summation_index.append((i, indices[i]))
            elif isinstance(k, (int, str, Expression)):
                indices.append(k)

        term = Tensor(self.var_label, self.variable, self.shape, index_labels=indices)

        # for syntax-sugar x[:]
        for i, ind in summation_index:
            term = Sum({ind: self.shape[i]}, term)

        return term

    def __repr__(self) -> str:
        return self.var_label


