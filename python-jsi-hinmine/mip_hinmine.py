#!/usr/bin/env python3.6

'''
HINMine wrapper for the HBP medical platform.

@author: jan.kralj@ijs.si
'''

import logging
from mip_helper import io_helper, parameters, shapes

import numpy as np
import pandas as pd
import scipy.sparse as sp
import networkx as nx
import json
from profilehooks import timecall

import cf_netSDM


def adjacency_distance(vector_1, vector_2):
    v = vector_1 - vector_2
    return np.exp(-np.dot(v, v))


@timecall
def construct_adjacency_graph(item_names, item_features, item_labels):
    graph = nx.Graph()
    for item_name, item_label in zip(item_names, item_labels):
        graph.add_node(item_name, type='basic')
        graph.node[item_name]['labels'] = str(item_label)
    structure = cf_netSDM.lib.HIN.HeterogeneousInformationNetwork(graph, ',')
    structure.split_to_indices(train_indices=range(len(structure.node_list)))

    n = len(structure.node_list)
    matrix = np.zeros((n, n))
    for i in range(n):
        if i % 100 == 0:
            logging.info('Finished %i' % i)
        for j in range(n):
            d = adjacency_distance(item_features[i], item_features[j])
            structure.graph.add_edge(item_names[i], item_names[j], weight=d)
            matrix[i, j] = d
    structure.decomposed['decomposition'] = sp.csr_matrix(matrix)
    structure.basic_type = 'basic'
    return structure


@timecall
def _construct_results(propositionalized):
    n = propositionalized.shape[0]
    data = pd.DataFrame(propositionalized, columns=["f_{}".format(i + 1) for i in range(n)])

    logging.info('Rounding to 4 decimal places to reduce size of a final object')
    data = data.round(4)

    data['id'] = range(len(data))

    results_dict = {
        'profile': 'tabular-data-resource',
        'name': 'hinmine-features',
        'data': data.to_dict(orient='records'),
        'schema': {
            'fields': [],
            'primaryKey': 'id'
        }
    }

    for col_index in range(n):
        results_dict['schema']['fields'].append({'name': 'f_{}'.format(col_index + 1), 'type': 'float'})

    return results_dict


def main():
    # configure logging
    logging.basicConfig(level=logging.INFO)
    logging.info(cf_netSDM)
    # Read inputs
    data = io_helper.fetch_data()['data']
    X = io_helper.fetch_dataframe(data['independent'])
    y = io_helper.fetch_dataframe(data['dependent']).iloc[:, 0]

    if len(X) >= 2000:
        logging.warning('HINMine runs in quadratic time, processing {} samples could be very slow.'.format(len(X)))

    normalize = parameters.get_param('normalize', bool, 'True')
    damping = parameters.get_param('damping', float, '0.85')

    if normalize:
        X = X.apply(lambda x: x / np.linalg.norm(x))

    network = construct_adjacency_graph(range(len(X)), X.values, y.values)
    propositionalized = timecall(cf_netSDM.hinmine_propositionalize)(network, damping)['train_features']['data']

    results_dict = _construct_results(propositionalized)

    io_helper.save_results(json.dumps(results_dict), shapes.Shapes.TEXT)


if __name__ == '__main__':
    main()
