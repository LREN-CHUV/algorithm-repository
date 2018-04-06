#!/usr/bin/env python3.6

'''
HINMine wrapper for the HBP medical platform.

@author: jan.kralj@ijs.si
'''

import logging
from mip_helper import io_helper

import numpy as np
import scipy.sparse as sp
import networkx as nx
import json

import cf_netSDM


def adjacency_distance(vector_1, vector_2):
    v = vector_1 - vector_2
    return np.exp(-np.dot(v, v))


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


def main():
    # configure logging
    logging.basicConfig(level=logging.INFO)
    logging.info(cf_netSDM)
    # Read inputs
    inputs = io_helper.fetch_data()
    data = inputs['data']
    normalize = io_helper.get_param(inputs['parameters'], 'normalize', bool, 'True')
    damping = io_helper.get_param(inputs['parameters'], 'damping', float, '0.85')
    data_array = np.zeros((len(data['independent'][0]['series']), len(data['independent'])))
    col_number = 0
    row_number = 0
    for var in data['independent']:
        for value in var['series']:
            data_array[row_number, col_number] = value
            row_number += 1
        col_number += 1
        row_number = 0
    if normalize:
        for col_number in range(data_array.shape[1]):
            data_array[:, col_number] = data_array[:, col_number] / np.linalg.norm(data_array[:, col_number])
    network = construct_adjacency_graph(range(data_array.shape[0]), data_array, data['dependent'][0]['series'])
    propositionalized = cf_netSDM.hinmine_propositionalize(network, damping)['train_features']['data']
    results_dict = {
        'profile': 'tabular-data-resource',
        'name': 'hinmine-features',
        'data': [],
        'schema': {
            'fields': [],
            'primaryKey': 'id'
        }
    }
    n = propositionalized.shape[0]
    for row_index in range(n):
        instance = {"id": row_index}
        for col_index in range(n):
            instance["feature_%i" % (col_index + 1)] = propositionalized[row_index, col_index]
        results_dict['data'].append(instance)
    for col_index in range(n):
        results_dict['schema']['fields'].append({'name': 'feature_%i' % (col_index + 1), 'type': 'float'})
    io_helper.save_results(json.dumps(results_dict), '', 'text/plain')


if __name__ == '__main__':
    main()
