# TODO: move to a separate repository or at least python-mip
from sklearn.linear_model import SGDRegressor


def sklearn_to_pfa(estimator, types):
    """
    Convert scikit-learn estimator to PrettyPFA format.
    :param estimator: Scikit-learn estimator, must be supported
    :param types: List of tuples (name, type)

    Example output:
        input: record(Data,
            feature0: double,
            feature1: double,
        )
        output: double
        action:
            -2.525797382870301 + 31.7004451488 * input.feature0 + 42.5005713274 * input.feature1
    """
    if not _is_supported(estimator):
        raise NotImplementedError('Estimator {} is not yet supported'.format(estimator.__class__.__name__))

    formula = _regression_formula(estimator, types)
    input_record = _input_record(types)

    pfa = """
input: {input_record}
output: double
action:
    {formula}
    """.format(
        input_record=input_record, formula=formula
    ).strip()

    return pfa


def _regression_formula(estimator, types):
    """
    Create regression formula from estimator's coefficients.

    Example output:
        1.2 + 3.45 * input.featureA + 6.78 * input.featureB
    """
    feature_names = ['input.' + c for c, _ in types]
    return ' + '.join(
        [str(estimator.intercept_[0])] + ['{} * {}'.format(a, b) for a, b in zip(estimator.coef_, feature_names)]
    )


def _input_record(types):
    s = 'record(Data'
    for name, typ in types:
        s += ',\n    {}: {}'.format(name, typ)
    return s + '\n)'


def _is_supported(estimator):
    return isinstance(estimator, (SGDRegressor, ))
