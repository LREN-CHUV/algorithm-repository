import mock
import json
from . import fixtures as fx


def test_main():
    io_helper = mock.MagicMock()
    with mock.patch.dict('sys.modules', io_helper=io_helper):
        from linear_regression import main
        mip_helper.io_helper.fetch_data.return_value = fx.inputs
        main()
        # TODO: fix numerical errors
        assert mip_helper.io_helper.save_results.assert_called_with(json.dumps(fx.outputs), '', 'application/json')
