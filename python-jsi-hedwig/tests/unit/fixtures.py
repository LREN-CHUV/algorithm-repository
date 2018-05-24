def data():
    return {
        'dependent': [
            {
                'name': 'alzheimerbroadcategory',
                'type': {
                    'name': 'polynominal',
                    'enumeration': ['AD', 'CN', 'Other'],
                    'enumeration_labels': ["Alzheimer's disease", 'Cognitively Normal', 'Other']
                },
                'series': ['AD', 'AD', 'Other', 'CN', 'CN', 'AD', 'AD', 'AD', 'CN', 'CN'],
                'label': 'alzheimerbroadcategory'
            }
        ],
        'independent': [
            {
                'name': 'lefthippocampus',
                'type': {
                    'name': 'real'
                },
                'series': [3.4613, 3.3827, 2.6429, 2.8996, 3.4736, 2.8842, 2.9821, 2.8124, 2.9098, 2.8485],
                'mean': 3.0,
                'std': 0.35,
                'label': 'lefthippocampus'
            }, {
                'name': 'subjectageyears',
                'type': {
                    'name': 'integer'
                },
                'series': [63, 67, 71, 69, 66, 75, 73, 69, 73, 79],
                'label': 'Age Years'
            }, {
                'name': 'apoe4',
                'type': {
                    'name': 'polynominal',
                    'enumeration': [0, 1, 2],
                    'enumeration_labels': [0, 1, 2]
                },
                'series': [0, 1, 2, 1, 1, 2, 1, 1, 2, 2],
                'label': 'ApoE4'
            }
        ]
    }


def hedwig_output():
    return """
'B'(X) <--
Organization(X), Financial_Failure_Term(X), Angela_Merkel(X) [cov=13, pos=9, prec=0.692, lift=2.564, pval=0.000]
Nicolas_Sarkozy(X), Bank(X) [cov=16, pos=11, prec=0.688, lift=2.546, pval=0.000]
    """.strip()
