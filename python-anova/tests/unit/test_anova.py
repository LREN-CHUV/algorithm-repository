import pytest
import mock
import json
import os
import logging
from anova import generate_formula, main
from mip_helper import errors
from mip_helper import testing as t


# def test_generate_formula():
#     """Raise error when factorial design and too many covariables are used."""
#     dep_var = {'name': 'dep'}
#     indep_vars = [{'name': str(i)} for i in range(10)]
#     with pytest.raises(errors.UserError):
#         generate_formula(dep_var, indep_vars, 'factorial')


# @mock.patch('anova.io_helper.fetch_data')
# @mock.patch('anova.io_helper.save_results')
# def test_main(mock_save_results, mock_fetch_data):
#     mock_fetch_data.return_value = t.inputs_regression(include_nominal=False)
#     main()
#     result = json.loads(mock_save_results.call_args[0][0])
#     assert t.round_dict(result) == {
#         'Residual': {
#             'F': 'NaN',
#             'PR(>F)': 'NaN',
#             'df': 1.0,
#             'mean_sq': 0.019,
#             'sum_sq': 0.019
#         },
#         'minimentalstate': {
#             'F': 12.831,
#             'PR(>F)': 0.173,
#             'df': 1.0,
#             'mean_sq': 0.248,
#             'sum_sq': 0.248
#         },
#         'subjectage': {
#             'F': 0.958,
#             'PR(>F)': 0.507,
#             'df': 1.0,
#             'mean_sq': 0.019,
#             'sum_sq': 0.019
#         },
#         'subjectage:minimentalstate': {
#             'F': 0.096,
#             'PR(>F)': 0.808,
#             'df': 1.0,
#             'mean_sq': 0.002,
#             'sum_sq': 0.002
#         }
#     }


# @mock.patch('anova.io_helper.fetch_data')
# @mock.patch('anova.io_helper.save_error')
# @mock.patch('sys.exit')
# def test_main_signular_matrix(mock_exit, mock_save_error, mock_fetch_data):
#     mock_fetch_data.return_value = t.inputs_regression(limit_to=1, include_nominal=False)
#     main()
#     mock_save_error.assert_called_with('Too many factors (4) for too little data (1). Use less covariables or different design.')


# @mock.patch('anova.io_helper.fetch_data')
# @mock.patch('anova.io_helper.save_error')
# @mock.patch('sys.exit')
# def test_main_empty_input(mock_exit, mock_save_error, mock_fetch_data):
#     mock_fetch_data.return_value = t.inputs_regression(limit_to=0)
#     main()

#     mock_exit.assert_called_once_with(1)
#     mock_save_error.assert_called_once()


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_my_data(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Balanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "III"
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert abs(result['Residual']['mean_sq']-2.6447) < 10e-5
    # assert t.round_dict(result) == {
    #     'Residual': {
    #         'F': 'NaN',
    #         'PR(>F)': 'NaN',
    #         'df': 171.0,
    #         'mean_sq': 2.6447,
    #         'sum_sq': 452.2500
    #     },
    #     'var_I1': {
    #         'F': 59258.7776,
    #         'PR(>F)': .0001,
    #         'df': 2.0,
    #         'mean_sq': 156723.8722,
    #         'sum_sq': 313447.7444
    #     },
    #     'var_I2': {
    #         'F': 2683.3693,
    #         'PR(>F)': .0001,
    #         'df': 2.0,
    #         'mean_sq': 7096.8056,
    #         'sum_sq': 14193.6111
    #     },
    #     'var_I1:var_I2': {
    #         'F': 5.9668,
    #         'PR(>F)': 0.0002,
    #         'df': 4.0,
    #         'mean_sq': 15.7806,
    #         'sum_sq': 63.1222
    #     }
    # }
