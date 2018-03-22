# TODO: DRY with python-sgd-regressor -- fixtures could be available in `mip_helper` library as samples
import pytest


def independent(include_categorical=False, include_real=True):
    ret = []
    if include_real:
        ret += [
            {
                'name': 'stress_before_test1',
                'type': {
                    'name': 'real'
                },
                'label': 'Stress before test',
                'series': [
                    61.4698271904, 53.7560829699, 43.7334060431, 57.978654924, 51.4467006894, 49.1931665942
                ],
                'mean': 55,
                'std': 20.,
            }, {
                'name': 'iq',
                'type': {
                    'name': 'real'
                },
                'label': 'IQ',
                'series': [
                    73.5856470359, 73.6181456345, 73.7897320711, 73.8623274925, 73.9894228193, 74.4441778038
                ],
                'mean': 72,
                'std': 10.,
            }
        ]
    if include_categorical:
        ret.append({
            'name': 'agegroup',
            'type': {
                'name': 'polynominal',
                'enumeration': ['-50y', '50-59y', '59y-']
            },
            'label': 'Age group',
            'series': [
                '-50y', '50-59y', '-50y', '50-59y', '-50y', '50-59y'
            ]
        })
    return ret


@pytest.fixture
def inputs_regression(**kwargs):
    return {
        'data': {
            'dependent': [
                {
                    'name': 'score_test1',
                    'type': {
                        'name': 'real'
                    },
                    'label': 'Score test',
                    'series': [
                        846.2601464093, 1257.859885233, 1070.6406427181, 1040.8477167398, 1173.4546177907, 1189.9664245547
                    ]
                }
            ],
            'independent': independent(**kwargs)
        },
        'parameters': []
    }


@pytest.fixture
def inputs_classification(**kwargs):
    return {
        'data': {
            'dependent': [
                {
                    'name': 'score_test1',
                    'type': {
                        'name': 'polynominal',
                        'enumeration': ['AD', 'CN', 'Other']
                    },
                    'label': 'Score test',
                    'series': [
                        'AD', 'CN', 'Other', 'AD', 'CN', 'Other'
                    ]
                }
            ],
            'independent': independent(**kwargs)
        },
        'parameters': []
    }
