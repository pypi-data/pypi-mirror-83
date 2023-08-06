class Variable:
    def __init__(self, var_name, var_kind, var_aggregation_tsx,
                 var_filter_tsx, var_interpolation):
        self.var_name = var_name
        self.var_kind = var_kind
        self.var_aggregation_tsx = var_aggregation_tsx
        self.var_filter_tsx = var_filter_tsx
        self.var_interpolation = var_interpolation

    def as_dict(self):
        """
        Represent the current Variable as a dict

        The returned dict should be valid for serialization and
        passing back to TSI or for creating new variables.

        Returns
        -------
        dict
            Variable stored as a python dict
        """
        var_description = {'kind': self.var_kind}
        if self.var_filter_tsx is not None:
            var_description['filter'] = {'tsx': self.var_filter_tsx}
        if self.var_aggregation_tsx is not None:
            var_description['aggregation'] = {'tsx': self.var_aggregation_tsx}
        if self.var_interpolation is not None:
            var_description['interpolation'] = self.var_interpolation

        return {self.var_name: var_description}

    def copy(self):
        """
        Create a copy of the Variable

        Returns
        -------
        Variable
                Copied object
        """
        return Variable(var_name=self.var_name,
                        var_kind=self.var_kind,
                        var_aggregation_tsx=self.var_aggregation_tsx,
                        var_filter_tsx=self.var_filter_tsx,
                        var_interpolation=self.var_interpolation)

    def __repr__(self):
        return f'<{self.var_kind} variable {self.var_name}>'


class NumericVariable(Variable):
    def __init__(self, var_name, var_kind, var_aggregation_tsx,
                 var_filter_tsx, var_interpolation, var_value_tsx):
        super(NumericVariable, self).__init__(var_name=var_name,
                                              var_kind=var_kind,
                                              var_aggregation_tsx=var_aggregation_tsx,
                                              var_filter_tsx=var_filter_tsx,
                                              var_interpolation=var_interpolation)
        self.var_value_tsx = var_value_tsx

    def copy(self):
        """
        Create a copy of the Variable

        Returns
        -------
        Variable
                Copied object
        """
        return NumericVariable(var_name=self.var_name,
                               var_kind=self.var_kind,
                               var_value_tsx=self.var_value_tsx,
                               var_aggregation_tsx=self.var_aggregation_tsx,
                               var_filter_tsx=self.var_filter_tsx,
                               var_interpolation=self.var_interpolation)

    def as_dict(self):
        """
        Represent the current Variable as a dict

        The returned dict should be valid for serialization and
        passing back to TSI or for creating new variables.

        Returns
        -------
        dict
            Variable stored as a python dict
        """
        var_description = super(NumericVariable, self).as_dict()[self.var_name]
        var_description['value'] = {'tsx': self.var_value_tsx}

        return {self.var_name: var_description}


def variable_helper(var_name, var_info):
    """
    Helper function which returns the appropriate Variable object given
    a TSI server response.
    """
    var_kind = var_info['kind']
    var_value = var_info.get('value')
    var_value_tsx = var_value['tsx'] if var_value is not None else None
    var_filter = var_info.get('filter')
    var_filter_tsx = var_filter['tsx'] if var_filter is not None else None
    var_aggregation = var_info.get('aggregation')
    var_aggregation_tsx = var_aggregation['tsx'] if var_aggregation is not None else None
    var_interpolation = var_info.get('interpolation')

    # Create the appropriate Variable types
    if var_kind == 'aggregate':
        return Variable(var_name=var_name,
                        var_kind=var_kind,
                        var_aggregation_tsx=var_aggregation_tsx,
                        var_filter_tsx=var_filter_tsx,
                        var_interpolation=var_interpolation)
    elif var_kind == 'numeric':
        return NumericVariable(var_name=var_name,
                               var_kind=var_kind,
                               var_aggregation_tsx=var_aggregation_tsx,
                               var_filter_tsx=var_filter_tsx,
                               var_interpolation=var_interpolation,
                               var_value_tsx=var_value_tsx)
    else:
        # Notably we do not yet support Categorical vars
        return RuntimeError(f'Variable type {var_kind} not yet supported')
