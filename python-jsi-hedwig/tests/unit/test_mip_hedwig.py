import mock
from mip_hedwig import main
from . import fixtures as fx


def _write_file(cmds):
    out_name = cmds[cmds.index('-o') + 1]
    with open(out_name, 'w') as f:
        f.write(fx.hedwig_output())


@mock.patch('mip_hedwig.io_helper.fetch_data')
@mock.patch('mip_hedwig.io_helper.save_results')
@mock.patch('mip_hedwig.call')
def test_main(mock_call, mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = {'data': fx.data()}
    mock_call.side_effect = _write_file
    main(clean_files=True)
    ret = mock_save_results.call_args[0][0]
    assert ret == "'B'(X) <--\nOrganization(X), Financial_Failure_Term(X), Angela_Merkel(X) [cov=13, pos=9, prec=0.692, lift=2.564, pval=0.000]\nNicolas_Sarkozy(X), Bank(X) [cov=16, pos=11, prec=0.688, lift=2.546, pval=0.000]"
