def independent(include_categorical=False, limit_from=0, limit_to=20):
    ret = [
        {
            'name':
            'stress_before_test1',
            'type': {
                'name': 'real'
            },
            'series': [
                61.81, 58.63, 37.61, 42.44, 29.06, 26.28, 53.34, 90.5, 61.87, 62.67, 56.71, 72.7, 64.77, 65.79, 72.68,
                65.44, 94.5, 84.3, 53.97, 66.1
            ][limit_from:limit_to],
            'mean':
            55,
            'std':
            20.,
            'minValue':
            35,
            'maxValue':
            75,
        }, {
            'name':
            'iq',
            'type': {
                'name': 'real'
            },
            'series': [
                62.94, 79.34, 77.9, 77.69, 61.53, 76.44, 65.89, 68.81, 72.55, 65.53, 71.97, 65.89, 61.04, 77.79, 46.78,
                56.21, 78.11, 59.72, 67.47, 75.55
            ][limit_from:limit_to],
            'mean':
            72,
            'std':
            10.,
            'minValue':
            60,
            'maxValue':
            80,
        }
    ]
    if include_categorical:
        ret.append(
            {
                'name':
                'agegroup',
                'type': {
                    'name': 'polynominal',
                    'enumeration': ['-50y', '50-59y']
                },
                'label':
                'Age Group',
                'series': [
                    '-50y', '-50y', '-50y', '50-59y', '-50y', '50-59y', '-50y', '50-59y', '-50y', '50-59y', '-50y',
                    '50-59y', '-50y', '50-59y', '-50y', '50-59y', '-50y', '50-59y', '-50y', '50-59y'
                ][limit_from:limit_to]
            }
        )
    return ret


def inputs_regression(add_null=False, limit_from=0, limit_to=1000000, **kwargs):
    data = {
        'data': {
            'dependent': [
                {
                    'name':
                    'score_test1',
                    'label':
                    'Score test 1',
                    'type': {
                        'name': 'real'
                    },
                    'series': [
                        1004.98, 1016.14, 999.9, 993.33, 957.59, 1023.14, 997.98, 981.09, 971.32, 1012.34, 1020.45,
                        1001.23, 1001.1, 1004.68, 1014.85, 1023.91, 972.02, 978.55, 1017.6, 970.4
                    ][limit_from:limit_to],
                    'mean':
                    1000.,
                    'std':
                    200.,
                    'minValue':
                    700.,
                    'maxValue':
                    1300.,
                }
            ],
            'independent':
            independent(limit_from=limit_from, limit_to=limit_to, **kwargs)
        },
        'parameters': []
    }
    if add_null:
        data['data']['dependent'][0]['series'][0] = None
    return data


def output():
    return {
        'agegroup_-50y': {
            'coef': -3.257,
            'p_values': 0.739,
            'std_err': 9.599,
            't_values': -0.339
        },
        'intercept': {
            'coef': 1045.541,
            'p_values': 0.0,
            'std_err': 46.866,
            't_values': 22.309
        },
        'iq': {
            'coef': -0.416,
            'p_values': 0.471,
            'std_err': 0.563,
            't_values': -0.739
        },
        'stress_before_test1': {
            'coef': -0.281,
            'p_values': 0.326,
            'std_err': 0.277,
            't_values': -1.013
        }
    }
