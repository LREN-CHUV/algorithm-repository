import pandas as pd
from sklearn_to_pfa.featurizer import Featurizer, OneHotEncoding, Standardize


def test_featurizer():
    transforms = [
        OneHotEncoding('c0', ['a', 'b']),
        Standardize('c1', 1, 2),
    ]
    featurizer = Featurizer(transforms)

    data = pd.DataFrame({
        'c0': ['a', 'a', 'b'],
        'c1': [1, 2, 3],
    })
    X = featurizer.transform(data)
    pfa = featurizer.generate_pretty_pfa()
    assert X.tolist() == [[1.0, 0.0, 0.0], [1.0, 0.0, 0.5], [0.0, 1.0, 1.0]]
    assert pfa == """
new(array(double),
    C(x.c0),
    arr((x.c1 - 1) / 2)
);""".strip()
