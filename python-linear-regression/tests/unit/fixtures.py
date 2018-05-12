def output_regression():
    return {
        'agegroup_-50y': {
            'coef': 0.183,
            'p_values': 0.14,
            'std_err': 0.041,
            't_values': 4.476
        },
        'intercept': {
            'coef': 2.513,
            'p_values': 0.048,
            'std_err': 0.189,
            't_values': 13.309
        },
        'minimentalstate': {
            'coef': 0.036,
            'p_values': 0.044,
            'std_err': 0.003,
            't_values': 14.404
        },
        'subjectage': {
            'coef': -0.005,
            'p_values': 0.275,
            'std_err': 0.003,
            't_values': -2.168
        }
    }


def output_classification():
    return {
        'AD': {
            'agegroup_-50y': {
                'coef': -0.248,
                'p_values': 0.693,
                'std_err': 0.627,
                't_values': -0.395
            },
            'intercept': {
                'coef': 0.224,
                'p_values': 0.941,
                'std_err': 3.007,
                't_values': 0.074
            },
            'minimentalstate': {
                'coef': 0.028,
                'p_values': 0.669,
                'std_err': 0.067,
                't_values': 0.427
            },
            'subjectage': {
                'coef': -0.023,
                'p_values': 0.56,
                'std_err': 0.039,
                't_values': -0.582
            }
        },
        'CN': {
            'agegroup_-50y': {
                'coef': 0.894,
                'p_values': 0.159,
                'std_err': 0.635,
                't_values': 1.408
            },
            'intercept': {
                'coef': 0.666,
                'p_values': 0.822,
                'std_err': 2.955,
                't_values': 0.226
            },
            'minimentalstate': {
                'coef': 0.034,
                'p_values': 0.601,
                'std_err': 0.065,
                't_values': 0.523
            },
            'subjectage': {
                'coef': -0.037,
                'p_values': 0.342,
                'std_err': 0.039,
                't_values': -0.95
            }
        },
        'Other': {
            'agegroup_-50y': {
                'coef': -0.65,
                'p_values': 0.296,
                'std_err': 0.623,
                't_values': -1.044
            },
            'intercept': {
                'coef': -3.055,
                'p_values': 0.3,
                'std_err': 2.946,
                't_values': -1.037
            },
            'minimentalstate': {
                'coef': -0.066,
                'p_values': 0.33,
                'std_err': 0.068,
                't_values': -0.974
            },
            'subjectage': {
                'coef': 0.061,
                'p_values': 0.135,
                'std_err': 0.041,
                't_values': 1.494
            }
        }
    }
