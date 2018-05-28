import pandas as pd
import preprocess
from . import fixtures as fx


def test_dump_to_csv(tmpdir):
    f = tmpdir.join('out.csv')
    matrix, attributes = preprocess.to_matrix(fx.data(), do_binarize=True, bins=4)
    preprocess.dump_to_csv(matrix, attributes, str(f))
    df = pd.read_csv(f, sep=';')
    assert len(df) == 10
    assert list(df.columns) == [
        'id', '2.6429less_than=lefthippocampusless_than2.850575', '2.850575less_than=lefthippocampusless_than3.05825',
        '3.05825less_than=lefthippocampusless_than3.2659249999999997',
        '3.2659249999999997less_than=lefthippocampusless_than3.4736', '63.0less_than=subjectageyearsless_than67.0',
        '67.0less_than=subjectageyearsless_than71.0', '71.0less_than=subjectageyearsless_than75.0',
        '75.0less_than=subjectageyearsless_than79.0', 'apoe4', 'alzheimerbroadcategory'
    ]
