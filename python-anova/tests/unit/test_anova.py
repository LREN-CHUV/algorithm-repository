import pytest
import mock
import json
import os
import logging
from anova import generate_formula, main
from mip_helper import errors
from mip_helper import testing as t


EPSILON = 10e-5

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

# --------------------------------------------------------------------------------
# --------- TEST ANOVA TYPE I - BALANCED DATA
# --------------------------------------------------------------------------------


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_balanced_data_anova_typeI_factorial_design_2VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Balanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "I"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : balanced_data_anova_typeI_factorial_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 171.0
    assert abs(result['Residual']['mean_sq']-2.6447) < EPSILON
    assert abs(result['Residual']['sum_sq']-452.2500) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-59258.7776) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    assert abs(result['C(var_I1, Sum)']['mean_sq']-156723.8722) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-313447.7444) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-2683.3693) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    assert abs(result['C(var_I2, Sum)']['mean_sq']-7096.8056) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-14193.6111) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-5.9668) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)']-0.0002) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-15.7806) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-63.1222) < EPSILON
 
 
@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_balanced_data_anova_typeI_factorial_design_3VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Balanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2, var_I3'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "I"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : balanced_data_anova_typeI_factorial_design_3VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 162.0
    assert abs(result['Residual']['mean_sq']-2.0204) < EPSILON
    assert abs(result['Residual']['sum_sq']-327.3000) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-77571.8524) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    assert abs(result['C(var_I1, Sum)']['mean_sq']-156723.8722) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-313447.7444) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-3512.6260) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    assert abs(result['C(var_I2, Sum)']['mean_sq']-7096.8056) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-14193.6111) < EPSILON

    assert abs(result['C(var_I3, Sum)']['F']-56.2301) < EPSILON
    assert result['C(var_I3, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I3, Sum)']['df'] == 1.0
    assert abs(result['C(var_I3, Sum)']['mean_sq']-113.6056) < EPSILON
    assert abs(result['C(var_I3, Sum)']['sum_sq']-113.6056) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-7.8107) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-15.7806) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-63.1222) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['F']-1.1907) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['PR(>F)']-0.3067) < EPSILON
    assert result['C(var_I1, Sum):C(var_I3, Sum)']['df'] == 2.0
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['mean_sq']-2.4056) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['sum_sq']-4.8111) < EPSILON

    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['F']-1.4546) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.2365) < EPSILON
    assert result['C(var_I2, Sum):C(var_I3, Sum)']['df'] == 2.0
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-2.9389) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-5.8778) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['F']-0.0811) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.9881) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['df'] == 4.0
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-0.1639) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-0.6556) < EPSILON 


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_balanced_data_anova_typeI_additive_design_2VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Balanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "I"
    os.environ['MODEL_PARAM_design'] = "additive"
    logging.info("---------- TEST : balanced_data_anova_typeI_additive_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 175.0
    assert abs(result['Residual']['mean_sq']-2.9450) < EPSILON
    assert abs(result['Residual']['sum_sq']-515.3722) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-53217.2214) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    assert abs(result['C(var_I1, Sum)']['mean_sq']-156723.8722) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-313447.7444) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-2409.7942) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    assert abs(result['C(var_I2, Sum)']['mean_sq']-7096.8056) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-14193.6111) < EPSILON



@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_balanced_data_anova_typeI_additive_design_3VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Balanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2, var_I3'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "I"
    os.environ['MODEL_PARAM_design'] = "additive"
    logging.info("---------- TEST : balanced_data_anova_typeI_additive_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 174.0
    assert abs(result['Residual']['mean_sq']-2.3090) < EPSILON
    assert abs(result['Residual']['sum_sq']-401.7667) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-67875.1027) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    assert abs(result['C(var_I1, Sum)']['mean_sq']-156723.8722) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-313447.7444) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-3073.5356) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    assert abs(result['C(var_I2, Sum)']['mean_sq']-7096.8056) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-14193.6111) < EPSILON

    assert abs(result['C(var_I3, Sum)']['F']-49.2011) < EPSILON
    assert result['C(var_I3, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I3, Sum)']['df'] == 1.0
    assert abs(result['C(var_I3, Sum)']['mean_sq']-113.6056) < EPSILON
    assert abs(result['C(var_I3, Sum)']['sum_sq']-113.6056) < EPSILON


# --------------------------------------------------------------------------------
# --------- TEST ANOVA TYPE II - UNBALANCED DATA
# --------------------------------------------------------------------------------


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_unbalanced_data_anova_typeII_factorial_design_2VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Unbalanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "II"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : unbalanced_data_anova_typeII_factorial_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 191.0
    #assert abs(result['Residual']['mean_sq']-2.7183) < EPSILON
    assert abs(result['Residual']['sum_sq']-519.2000) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-65103.6306) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum)']['mean_sq']-176972.8012) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-353945.6024) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-2995.2032) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum)']['mean_sq']-8141.9345) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-16283.8690) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-6.7395) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-18.3202) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-73.2810) < EPSILON


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_unbalanced_data_anova_typeII_factorial_design_3VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Unbalanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2, var_I3'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "II"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : unbalanced_data_anova_typeII_factorial_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] ==182.0
 #   assert abs(result['Residual']['mean_sq']-2.0451) < EPSILON
    assert abs(result['Residual']['sum_sq']-372.2000) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-86536.9420) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum)']['mean_sq']-176972.8012) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-353945.6024) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-3981.2791) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum)']['mean_sq']-8141.9345) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-16283.8690) < EPSILON

    assert abs(result['C(var_I3, Sum)']['F']-65.7586) < EPSILON
    assert result['C(var_I3, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I3, Sum)']['df'] == 1.0
    #assert abs(result['C(var_I3, Sum)']['mean_sq']-134.4800) < EPSILON
    assert abs(result['C(var_I3, Sum)']['sum_sq']-134.4800) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-8.9583) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-18.3202) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-73.2810) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['F']-1.1759) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['PR(>F)']-0.3109) < EPSILON
    assert result['C(var_I1, Sum):C(var_I3, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['mean_sq']-2.4048) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['sum_sq']-4.8095) < EPSILON

    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['F']-1.6975) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.1860) < EPSILON
    assert result['C(var_I2, Sum):C(var_I3, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-3.4714) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-6.9429) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['F']-0.0803) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.9883) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-0.1643) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-0.6571) < EPSILON 
 
 

# --------------------------------------------------------------------------------
# --------- TEST ANOVA TYPE III - UNBALANCED DATA
# --------------------------------------------------------------------------------


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_unbalanced_data_anova_typeII_factorial_design_2VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Unbalanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "III"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : unbalanced_data_anova_typeII_factorial_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] == 191.0
    #assert abs(result['Residual']['mean_sq']-2.7183) < EPSILON
    assert abs(result['Residual']['sum_sq']-519.2000) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-63053.2335) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum)']['mean_sq']-171399.1562) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-342798.3125) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-2858.5890) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum)']['mean_sq']-7770.5729) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-15541.1458) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-6.7395) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-18.3202) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-73.2810) < EPSILON


@mock.patch('anova.io_helper.save_error')
@mock.patch('anova.io_helper.save_results')
def test_main_unbalanced_data_anova_typeII_factorial_design_3VI(mock_save_results, mock_save_error):
    os.environ['INPUT_FILE'] = 'tests/unit/Data/data_ANOVA_Unbalanced_with_inter_V1V2.csv'
    os.environ['PARAM_variables'] = 'var_D'
    os.environ['PARAM_covariables'] = 'var_I1, var_I2, var_I3'
    os.environ['PARAM_meta'] = '{"var_D":{"label":"VD","code":"var_D","type":"real"},"var_I1":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI1","code":"var_I1","type":"polynominal"},"var_I2":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"},{"code":"2","label":"2"}],"label":"VI2","code":"var_I2","type":"polynominal"},"var_I3":{"enumerations":[{"code":"0","label":"0"},{"code":"1","label":"1"}],"label":"VI3","code":"var_I3","type":"polynominal"}}'   
    os.environ['MODEL_PARAM_type'] = "III"
    os.environ['MODEL_PARAM_design'] = "factorial"
    logging.info("---------- TEST : unbalanced_data_anova_typeII_factorial_design_2VI")
    main()
    result = json.loads(mock_save_results.call_args[0][0])
    assert result['Residual']['F'] == 'NaN'
    assert result['Residual']['PR(>F)'] == 'NaN'
    assert result['Residual']['df'] ==182.0
 #   assert abs(result['Residual']['mean_sq']-2.0451) < EPSILON
    assert abs(result['Residual']['sum_sq']-372.2000) < EPSILON

    assert abs(result['C(var_I1, Sum)']['F']-83811.5165) < EPSILON
    assert result['C(var_I1, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum)']['mean_sq']-171399.1562) < EPSILON
    assert abs(result['C(var_I1, Sum)']['sum_sq']-342798.3125) < EPSILON

    assert abs(result['C(var_I2, Sum)']['F']-3799.6891) < EPSILON
    assert result['C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I2, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum)']['mean_sq']-7770.5729) < EPSILON
    assert abs(result['C(var_I2, Sum)']['sum_sq']-15541.1458) < EPSILON

    assert abs(result['C(var_I3, Sum)']['F']-58.8191) < EPSILON
    assert result['C(var_I3, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I3, Sum)']['df'] == 1.0
    #assert abs(result['C(var_I3, Sum)']['mean_sq']-120.2882) < EPSILON
    assert abs(result['C(var_I3, Sum)']['sum_sq']-120.2882) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['F']-8.9583) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['PR(>F)'] < .0001
    assert result['C(var_I1, Sum):C(var_I2, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['mean_sq']-18.3202) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum)']['sum_sq']-73.2810) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['F']-1.1766) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['PR(>F)']-0.3107) < EPSILON
    assert result['C(var_I1, Sum):C(var_I3, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['mean_sq']-2.4062) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I3, Sum)']['sum_sq']-4.8125) < EPSILON

    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['F']-1.6167) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.2014) < EPSILON
    assert result['C(var_I2, Sum):C(var_I3, Sum)']['df'] == 2.0
    #assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-3.3062) < EPSILON
    assert abs(result['C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-6.6125) < EPSILON

    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['F']-0.0803) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['PR(>F)']-0.9883) < EPSILON
    assert result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['df'] == 4.0
    #assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['mean_sq']-0.1643) < EPSILON
    assert abs(result['C(var_I1, Sum):C(var_I2, Sum):C(var_I3, Sum)']['sum_sq']-0.6571) < EPSILON 
 