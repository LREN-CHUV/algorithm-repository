import mock
import titus.prettypfa
from mip_helper import testing as t
from feature_importance import main
from . import fixtures as fx


@mock.patch('feature_importance.io_helper.fetch_data')
@mock.patch('feature_importance.io_helper.load_intermediate_json_results')
@mock.patch('feature_importance.io_helper.save_results')
def test_main(mock_save_results, mock_load_intermediate_json_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=False)

    pretty_pfa = fx.pretty_pfa_regression()
    pfa_dict = titus.prettypfa.jsonNode(pretty_pfa)
    mock_load_intermediate_json_results.return_value = [
        pfa_dict
    ]

    main('1')
    svg = mock_save_results.call_args[0][0]
    assert svg.strip().endswith('</svg>')
