#!/usr/bin/env python3

from io_helper import io_helper

import logging
import pandas


OUTPUT_SCHEMA = {
        'schema': {
            'field': [
                {'name': 'index', 'type': 'string'},
                {'name': 'count', 'type': 'object'},
                {'name': 'mean', 'type': 'number'},
                {'name': 'std', 'type': 'number'},
                {'name': 'min', 'type': 'number'},
                {'name': '25%', 'type': 'number'},
                {'name': '50%', 'type': 'number'},
                {'name': '75%', 'type': 'number'},
                {'name': 'max', 'type': 'number'}
            ]
        },
        'data': []
    }


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    data = list()
    data.append({
        'name': inputs['data']['dependent'][0]['name'],
        'type': inputs['data']['dependent'][0]['type']['name'],
        'values': pandas.DataFrame({inputs['data']['dependent'][0]['name']: inputs['data']['dependent'][0]['series']})
    })
    for variable in inputs['data']['independent']:
        data.append({
            'name': variable['name'],
            'type': variable['type']['name'],
            'values': pandas.DataFrame({variable['name']: variable['series']})
        })

    # Generate results
    logging.info("Generating results...")
    results = OUTPUT_SCHEMA
    for var_data in data:
        result = var_data['values'].describe(include='all').to_dict()[var_data['name']]
        result['index'] = var_data['name']
        if is_nominal(var_data['type']):
            count = var_data['values'].ix[:, 0].value_counts().transpose().to_dict()
            count.update({'all': sum(count.values())})
            result['count'] = count
        else:
            result['count'] = {'all': result['count']}
        results['data'].append(result)
    logging.info("Results: " + str(results))
    io_helper.save_results(pandas.json.dumps(results), '', 'application/vnd.dataresource+json')

    logging.info("DONE")


def is_nominal(var_type):
    return var_type in ['binominal', 'polynominal']


def update_schema_field(fields, name, value):
    for field in fields:
        if field['name'] == name:
            field['type'] = value


if __name__ == '__main__':
    main()
