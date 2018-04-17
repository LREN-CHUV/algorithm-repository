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
                'series': [
                    'AD', 'AD', 'Other', 'CN', 'CN', 'AD', 'AD', 'AD', 'CN', 'CN'
                ],
                'label': 'alzheimerbroadcategory'
            }
        ],
        'independent': [
            {
                'name': 'lefthippocampus',
                'type': {
                    'name': 'real'
                },
                'series': [
                    3.4613, 3.3827, 2.6429, 2.8996, 3.4736, 2.8842, 2.9821, 2.8124, 2.9098, 2.8485
                ],
                'mean': 3.0,
                'std': 0.35,
                'label': 'lefthippocampus'
            }, {
                'name': 'subjectageyears',
                'type': {
                    'name': 'integer'
                },
                'series': [
                    63, 67, 71, 69, 66, 75, 73, 69, 73, 79
                ],
                'label': 'Age Years'
            }
        ]
    }
