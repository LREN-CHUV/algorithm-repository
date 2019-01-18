import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import patsy
import json
import mock
import os

from mip_helper import testing as t
from distributed_anova import anova_models, intermediate_models, aggregate_models, intermediate_anova, aggregate_anova, _sum_of_squares
from anova import main


def _generate_data(k=50, random_state=None):
    if random_state:
        np.random.seed(random_state)
    return pd.DataFrame(
        {
            'a': 10 * np.random.random(k),
            'b': np.random.choice(['x', 'y', 'z'], k),
            'c': np.random.choice(['x', 'y'], k),
        }
    )


def test_anova_models():
    df = _generate_data(random_state=42)
    formula = "a ~ C(c) * C(b)"

    # get ANOVA from statsmodels
    slm = ols(data=df, formula=formula).fit()
    sm_anova = anova_lm(slm)

    # create nested models
    y, X = patsy.dmatrices(formula, data=df, return_type='dataframe')
    y = y.iloc[:, 0]

    XtX = X.T.values @ X.values
    Xty = X.T.values @ y.values

    # fit submodels
    sub_ss = []
    for k in range(1, X.shape[1] + 1):
        beta = np.linalg.pinv(XtX[:k, :k]) @ Xty[:k]
        y_hat = X.values[:, :k] @ beta

        ss = {'dof': len(X) - sum(abs(beta) > 1e-10), 'columns': X.columns[:k], **_sum_of_squares(y_hat, y, y.mean())}
        sub_ss.append(ss)

    mm_anova = anova_models(sub_ss)

    for c in sm_anova.columns:
        assert (sm_anova[c] - mm_anova[c]).abs().sum() < 1e-3


def _inputs_regression(*args, columns=None, **kwargs):
    out = t.inputs_regression(*args, **kwargs)
    if columns:
        out['data']['independent'] = [v for v in out['data']['independent'] if v['name'] in columns]

    return out


@mock.patch('distributed_anova.io_helper.fetch_data')
@mock.patch('distributed_anova.io_helper.load_intermediate_json_results')
@mock.patch('distributed_anova.io_helper.save_results')
def test_distributed_anova(mock_save_results, mock_load_intermediate_json_results, mock_fetch_data):
    """Test that goes through all steps of distributed anova."""
    # columns = ['minimentalstate', 'agegroup']
    columns = ['agegroup']

    # run partial jobs
    inputs_1 = _inputs_regression(limit_from=0, limit_to=8, include_nominal=True, columns=columns)
    mock_fetch_data.return_value = inputs_1
    intermediate_models()
    output_1 = mock_save_results.call_args[0][0]

    inputs_2 = _inputs_regression(limit_from=8, limit_to=20, include_nominal=True, columns=columns)
    mock_fetch_data.return_value = inputs_2
    intermediate_models()
    output_2 = mock_save_results.call_args[0][0]

    mock_load_intermediate_json_results.return_value = [json.loads(output_1), json.loads(output_2)]

    # get model parameters
    aggregate_models(['1', '2'])
    submodels = json.loads(mock_save_results.call_args[0][0])

    # calculate sum of squares on nodes
    mock_fetch_data.return_value = inputs_1
    mock_load_intermediate_json_results.return_value = [submodels]
    intermediate_anova('3')
    output_1 = mock_save_results.call_args[0][0]

    mock_fetch_data.return_value = inputs_2
    mock_load_intermediate_json_results.return_value = [submodels]
    intermediate_anova('3')
    output_2 = mock_save_results.call_args[0][0]

    # aggregate sum of squares into ANOVA table
    mock_load_intermediate_json_results.return_value = [json.loads(output_1), json.loads(output_2)]

    # get model parameters
    aggregate_anova(['4', '5'])
    anova_dist = json.loads(mock_save_results.call_args[0][0])

    # ANOVA on single node
    mock_fetch_data.return_value = _inputs_regression(limit_to=20, include_nominal=True, columns=columns)
    os.environ['MODEL_PARAM_type'] = "I"
    os.environ['MODEL_PARAM_design'] = "factorial"
    main()
    anova_single = json.loads(mock_save_results.call_args[0][0])

    assert t.round_dict(anova_dist, 4) == t.round_dict(anova_single, 4)
