#!/usr/bin/env python3

from io_helper import io_helper

import logging
import pandas


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    inputs = io_helper.fetch_data()

    # Load data into a Pandas dataframe
    data_dict = {inputs['data']['dependent'][0]['name']: inputs['data']['dependent'][0]['series']}
    for variable in inputs['data']['independent']:
        data_dict.update({variable['name']: variable['series']})
    df = pandas.DataFrame(data_dict)
    io_helper.save_results(df.describe().to_json(), '', 'application/json')


if __name__ == '__main__':
    main()
