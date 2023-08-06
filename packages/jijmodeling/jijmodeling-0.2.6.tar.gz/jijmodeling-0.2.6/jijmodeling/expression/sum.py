from jijmodeling.expression.from_serializable import from_serializable
from jijmodeling.expression.expression import Add, Expression, _latex_repr

class Sum(Expression):
    def __init__(self, indices: dict, term):
        super().__init__(children=[term])
        self.indices = indices
        index_keys = list(indices.keys())
        self.index_labels = [ind for ind in self.index_labels if ind not in index_keys]

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.indices.keys():
            repr_str += str(i) + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__()) 
        return repr_str

    def __make_latex__(self):
        ind_str = ""
        ind_end = ""
        for ind, ind_set in self.indices.items():
            ind_latex = _latex_repr(ind)
            ind_conds = []
            if len(ind_latex.split(' ')) == 3:
                ind_conds = ind_latex.split(' ')[1:]
                ind_latex = ind_latex.split(' ')[0]
            from jijmodeling.variables.array import Array
            if isinstance(ind_set, Array):
                ind_str += "{} \in {}, ".format(ind_latex, _latex_repr(ind_set))
            elif isinstance(ind_set, tuple):
                iset0 = _latex_repr(ind_set[0])
                ind_end += _latex_repr(ind_set[1]) + '- 1' + ", "
                ind_str += "{} = {}".format(ind_latex, iset0) + ", "
            else:
                ind_end += _latex_repr(ind_set) + '- 1' + ", "
                ind_str += "{} = 0".format(ind_latex) + ", "

            if len(ind_conds) > 0:
                cond_latex = {'!=': '\\neq', '==': '=', '<=': '\leq', '>=': '\geq', '<': '<', '>': '>'}
                ind_str = ind_str[:-2]
                ind_str += '({} {} {}), '.format(ind_latex, cond_latex[ind_conds[0]], ind_conds[1])

        if isinstance(self.children[0], Add):
            term = _latex_repr(self.children[0])
        else:
            term = _latex_repr(self.children[0], False)

        return  "\sum_{{{}}}^{{{}}} {}".format(ind_str[:-2], ind_end[:-2], term)
        

    @classmethod
    def from_serializable(cls, serializable: dict):
        indices:dict = from_serializable(serializable['attributes']['indices'])
        term = from_serializable(serializable['attributes']['children'])[0]
        return cls(indices, term)