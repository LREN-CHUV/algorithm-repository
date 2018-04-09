'''
Hedwig wrapper for the HBP medical platform.

@author: anze.vavpetic@ijs.si
'''

import tempfile
import logging
from subprocess import call
from mip_helper import io_helper, parameters


import preprocess

DEFAULT_DOCKER_IMAGE = 'python-jsi-hedwig'


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    inputs = io_helper.fetch_data()
    data = inputs["data"]

    beam = parameters.get_param('beam', int, 10)
    support = parameters.get_param('support', float, '0.00001')
    out_file = 'input.csv'
    rules_out_file = 'rules.txt'

    matrix, attributes = preprocess.to_matrix(data)
    preprocess.dump_to_csv(matrix, attributes, out_file)

    # Call hedwig with sensible defaults
    examples_file = out_file

    empty_bk = tempfile.mkdtemp()
    call([
        'python', '-m' 'hedwig.__main__',
        empty_bk,
        examples_file,
        '--beam', str(beam),
        '--support', str(support),
        '-f', 'csv',
        '-l',
        '-o', rules_out_file,
        '--nocache'
    ])

    with open(rules_out_file) as f:
        results = f.read()
    # TODO: add text/plain to mime types in shapes.Shapes
    io_helper.save_results(results.replace('less_than', '<'), 'text/plain')
