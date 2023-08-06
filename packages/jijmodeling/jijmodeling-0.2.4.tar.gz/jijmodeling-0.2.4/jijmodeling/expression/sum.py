from jijmodeling.expression.from_serializable import from_serializable
from jijmodeling.expression.expression import Expression

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

    @classmethod
    def from_serializable(cls, serializable: dict):
        indices:dict = from_serializable(serializable['attributes']['indices'])
        term = from_serializable(serializable['attributes']['children'])[0]
        return cls(indices, term)