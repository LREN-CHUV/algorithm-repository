import pytest
from anova import generate_formula
from mip_helper import errors


def test_generate_formula():
    """Raise error when factorial design and too many covariables are used."""
    dep_var = {'name': 'dep'}
    indep_vars = [{'name': str(i)} for i in range(10)]
    with pytest.raises(errors.UserError):
        generate_formula(dep_var, indep_vars, 'factorial')
