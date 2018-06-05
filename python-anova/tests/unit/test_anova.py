import pytest
import mock
import json
from anova import generate_formula, main
from mip_helper import errors
from mip_helper import testing as t


def test_generate_formula():
    """Raise error when factorial design and too many covariables are used."""
    dep_var = {'name': 'dep'}
    indep_vars = [{'name': str(i)} for i in range(10)]
    with pytest.raises(errors.UserError):
        generate_formula(dep_var, indep_vars, 'factorial')


@mock.patch('anova.io_helper.fetch_data')
@mock.patch('anova.io_helper.save_results')
def test_main(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=False)
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert t.round_dict(result)['data'] == [
        {
            'Degrees of freedom': 1,
            'F-value': 0.958,
            'P-value': '0.507',
            'Sum²': 0.019,
            'Variable': 'subjectage'
        }, {
            'Degrees of freedom': 1,
            'F-value': 12.831,
            'P-value': '0.173',
            'Sum²': 0.248,
            'Variable': 'minimentalstate'
        }, {
            'Degrees of freedom': 1,
            'F-value': 0.096,
            'P-value': '0.808',
            'Sum²': 0.002,
            'Variable': 'subjectage:minimentalstate'
        }, {
            'Degrees of freedom': 1,
            'Sum²': 0.019,
            'Variable': 'Residual'
        }
    ]


@mock.patch('anova.io_helper.fetch_data')
@mock.patch('anova.io_helper.save_error')
@mock.patch('sys.exit')
def test_main_signular_matrix(mock_exit, mock_save_error, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(limit_to=1, include_nominal=False)
    main()
    mock_save_error.assert_called_with(
        'Too many factors (4) for too little data (1). Use less covariables or different design.'
    )


@mock.patch('anova.io_helper.fetch_data')
@mock.patch('anova.io_helper.save_error')
@mock.patch('sys.exit')
def test_main_empty_input(mock_exit, mock_save_error, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(limit_to=0)
    main()

    mock_exit.assert_called_once_with(1)
    mock_save_error.assert_called_once()
