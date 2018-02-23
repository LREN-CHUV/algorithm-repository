from rdflib.graph import Graph
from .lib.converters import n3_to_nx, digraph_to_graph, nx_to_n3, n3_to_nx_hyper, nx_to_n3_hyper
from .lib.helpers import prepare, add_generalization_predicates, add_negatives_hyper, add_negatives_regular
from .lib.core import nx_pagerank, shrink_by_pr, shrink_hyper_by_pr,  page_rank, stochastic_normalization, \
    label_propagation, label_propagation_normalization
from networkx import read_gml
from .lib.HIN import HeterogeneousInformationNetwork
from collections import defaultdict
import numpy as np
import logging
#py3

def cf_netsdm_reduce(input_dict):
    if input_dict['hyper'] == 'true':
        to_graph, to_rdf, shrink, add_negatives = n3_to_nx_hyper, nx_to_n3_hyper, shrink_hyper_by_pr, add_negatives_hyper
    else:
        to_graph, to_rdf, shrink, add_negatives = n3_to_nx, nx_to_n3, shrink_by_pr, add_negatives_regular
    data = Graph()
    prepare(data)
    data.parse(data=input_dict['examples'], format='n3')
    for ontology in input_dict['bk_file']:
        data.parse(data=ontology, format='n3')
    full_network, positive_nodes, negative_annotations, generalization_predicates = to_graph(data, input_dict['target'])
    if not input_dict['directed'] == 'true':
        saved_directions = full_network
        full_network = digraph_to_graph(full_network)
    node_list = full_network.nodes()
    node_list.sort()
    scores, scores_dict = nx_pagerank(digraph_to_graph(full_network) if not input_dict['directed'] == 'true' else full_network, node_list, positive_nodes)
    if not input_dict['directed'] == 'true':
        full_network = saved_directions
    add_negatives(full_network, negative_annotations)
    if not input_dict['adv_removal'] == 'false':
        if input_dict['hyper'] == 'true':
            raise Exception('Naive node removal is not compatible with hypergraph network construction.')
        shrink(full_network, node_list, scores, float(input_dict['minimum_ranking']), positive_nodes, input_dict['interdependent_relations'], naive_removal=True)
    else:
        shrink(full_network, node_list, scores, float(input_dict['minimum_ranking']), positive_nodes, input_dict['interdependent_relations'])
    negative_nodes = set(negative_annotations.keys())
    rdf_network, rdf_annotations = to_rdf(full_network, positive_nodes, negative_nodes)

    add_generalization_predicates(rdf_network, generalization_predicates)
    return {'bk_file': rdf_network.serialize(format='n3'),
            'ex_file': rdf_annotations.serialize(format='n3')}





def cf_load_gml(input_dict):
    net = read_gml(input_dict['file'])
    logging.info('Read file')
    hin = HeterogeneousInformationNetwork(net, input_dict['label_delimiter'])
    train_indices = []
    test_indices = []
    for index, node in enumerate(hin.node_list):
        if len(hin.graph.node[node]['labels']) > 0:
            train_indices.append(index)
        else:
            test_indices.append(index)
    hin.split_to_indices(train_indices=train_indices, test_indices=test_indices)
    hin.create_label_matrix()
    return {'net': hin}  # , 'train_indices': train_indices, 'test_indices': test_indices}


def cf_hinmine_decompose(input_dict):
    return {'test': 'test'}


def cf_hinmine_decompose_post(postdata, input_dict, output_dict):
    try:
        cycles = postdata['cycle']
    except KeyError:
        raise Exception('No decomposition cycle selected')
    hin = input_dict['network']
    for cycle in cycles:
        cycle = cycle.split('_____')
        node_sequence = []
        edge_sequence = []
        for i in range(len(cycle)):
            if i % 2 == 0:
                node_sequence.append(cycle[i])
            else:
                edge_sequence.append(cycle[i])
        degrees = defaultdict(int)
        for item in hin.midpoint_generator(node_sequence, edge_sequence):
            for node in item:
                degrees[node] += 1
        hin.decompose_from_iterator('decomposition',
                                    input_dict['heuristic'],
                                    None,
                                    hin.midpoint_generator(node_sequence, edge_sequence),
                                    degrees=degrees)

        # save_sparse(tehin.decomposed['MAM_%s' % weighing], 'D:/imdb_data/MAM.%s_fold_%i.npz' % (weighing, fold))
        logging.info('%s done' % input_dict['heuristic'])

    return {'network': hin}


def cf_hinmine_propositionalize(input_dict):
    hin = input_dict['network']
    assert isinstance(hin, HeterogeneousInformationNetwork)
    n = hin.decomposed['decomposition'].shape[0]
    vectors = np.zeros((n, n))
    graph = stochastic_normalization(hin.decomposed['decomposition'])
    for index in range(n):
        pr = page_rank(graph, [index], try_shrink=True, damping=input_dict['damping'])
        norm = np.linalg.norm(pr, 2)
        if norm > 0:
            pr = pr / np.linalg.norm(pr, 2)
            vectors[index, :] = pr
    train_features = {
        'data': vectors[hin.train_indices, :],
        'target': hin.label_matrix[hin.train_indices, :],
        'target_names': [str(x) for x in hin.label_list],
        'DESCR': None
    }
    test_features = {
        'data': vectors[hin.test_indices, :],
        'target_names': [str(x) for x in hin.label_list],
        'DESCR': None
    }
    return {'train_features': train_features, 'test_features': test_features}


def cf_hinmine_label_propagation(input_dict, weights=None, alpha=0.85, semibalanced=None):
    hin = input_dict['network']
    assert isinstance(hin, HeterogeneousInformationNetwork)
    matrix = label_propagation_normalization(hin.decomposed['decomposition'])
    hin.create_label_matrix(weights=weights)
    propagated_matrix = label_propagation(matrix, hin.label_matrix, alpha)
    return {'result': propagated_matrix[hin.test_indices]}
