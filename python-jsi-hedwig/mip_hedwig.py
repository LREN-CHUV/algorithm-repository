'''
Hedwig wrapper for the HBP medical platform.

@author: anze.vavpetic@ijs.si
'''

import tempfile
import logging
from subprocess import call
from io_helper import io_helper

import preprocess

DEFAULT_DOCKER_IMAGE = 'python-jsi-hedwig'

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    inputs = io_helper.fetch_data()
    data = inputs["data"]

    out_file = 'input.csv'
    rules_out_file = 'rules.txt'

    matrix, attributes = preprocess.to_matrix(data)
    preprocess.dump_to_csv(matrix, attributes, out_file)

    # Call hedwig with sensible defaults
    examples_file = out_file

    empty_bk = tempfile.mkdtemp()
    call([
        'python', '-m', 'hedwig',
        empty_bk,
        examples_file,
        '-f', 'csv',
        '-l',
        '-o', rules_out_file,
        '--nocache'
    ])

    results = ''
    with open(rules_out_file) as f:
        results = f.read()

    io_helper.save_results(results, '', 'text/plain')
