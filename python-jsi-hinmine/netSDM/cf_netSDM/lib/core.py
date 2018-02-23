import networkx as nx
import numpy as np
import scipy.sparse as sp
import logging
from collections import defaultdict


def stochastic_normalization(matrix):
    logging.info('Creating google matrix...')
    matrix = matrix.tolil()
    try:
        matrix.setdiag(0)
    except TypeError:
        matrix.setdiag(np.zeros(matrix.shape[0]))
    matrix = matrix.tocsr()
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    d[nzs] = 1 / d[nzs]
    matrix = (sp.diags(d, 0).tocsc().dot(matrix)).transpose()
    logging.info('Google matrix created.')
    return matrix


def page_rank(matrix, start_nodes,
              epsilon=1e-6,
              max_steps=10000,
              damping=0.85,
              spread_step=10,
              spread_percent=0.5,
              try_shrink=True):
    assert(len(start_nodes)) > 0
    # this method assumes that column sums are all equal to 1 (stochastic normalizaition!)
    size = matrix.shape[0]
    if start_nodes is None:
        start_nodes = range(size)
        nz = size
    else:
        nz = len(start_nodes)
    start_vec = np.zeros((size, 1))
    start_vec[start_nodes] = 1
    start_rank = start_vec / len(start_nodes)
    rank_vec = start_vec / len(start_nodes)
    # calculate the max spread:
    shrink = False
    which = np.zeros(0)
    if try_shrink:
        v = start_vec / len(start_nodes)
        steps = 0
        while nz < size * spread_percent and steps < spread_step:
            steps += 1
            v += matrix.dot(v)
            nz_new = np.count_nonzero(v)
            if nz_new == nz:
                shrink = True
                break
            nz = nz_new
        rr = np.arange(matrix.shape[0])
        which = (v[rr] > 0).reshape(size)
        if shrink:
            start_rank = start_rank[which]
            rank_vec = rank_vec[which]
            matrix = matrix[:, which][which, :]
    diff = np.Inf
    steps = 0
    while diff > epsilon and steps < max_steps:  # not converged yet
        steps += 1
        new_rank = matrix.dot(rank_vec)
        rank_sum = np.sum(new_rank)
        if rank_sum < 0.999999999:
            new_rank += start_rank * (1 - rank_sum)
        new_rank = damping * new_rank + (1 - damping) * start_rank
        new_diff = np.linalg.norm(rank_vec - new_rank, 1)
        diff = new_diff
        rank_vec = new_rank
    if try_shrink and shrink:
        ret = np.zeros(size)
        ret[which] = rank_vec.reshape(rank_vec.shape[0])
        ret[start_nodes] = 0
        return ret.flatten()
    else:
        rank_vec[start_nodes] = 0
        return rank_vec.flatten()


def nx_pagerank(network, node_list, enriched_nodes):
    enriched_nodes = set(enriched_nodes)
    matrix = nx.to_scipy_sparse_matrix(network, dtype=float, nodelist=node_list, format='csr')
    enriched_indices = [i for i in range(len(node_list)) if node_list[i] in enriched_nodes]
    normalized_matrix = stochastic_normalization(matrix)

    pr = page_rank(normalized_matrix, enriched_indices, epsilon=1e-10, damping=0.99)

    pr_dict = {}
    for i in range(len(node_list)):
        pr_dict[node_list[i]] = pr[i]
    return pr, pr_dict


def shrink_by_pr(network, node_list, pr, percentage, enriched_symbols, interdependent_relations, naive_removal=False):
    if percentage < 1:
        new_node_list = []
        for node_index, node in enumerate(node_list):
            if node not in enriched_symbols:
                new_node_list.append((node, pr[node_index]))
        new_node_list.sort(key=lambda x: x[1], reverse=True)
        # threshold = new_node_list[int(percentage * len(new_node_list))]
        i = 1
        print(len(new_node_list))
        belows = defaultdict(set)
        for x in network:
            for node in network.edge[x]:
                belows[node].add(x)
        for node, score in new_node_list[int(percentage * len(new_node_list)):]:
            i += 1
            if node not in enriched_symbols:
                if naive_removal:
                    network.remove_node(node)
                else:
                    remove_regular(network, node, belows, interdependent_relations)


def remove_regular(network, node, belows, interdependent_relations):
    # below = [x for x in network if node in network.edge[x]]
    # print set(below) == set(belows[node])
    below = belows[node]
    above = network.edge[node].keys()
    relations = set([network.edge[x][node]['type'] for x in below])
    relations.update([network.edge[node][x]['type'] for x in above])
    if 'annotated_by' in relations:
        relations.remove('annotated_by')
    examples = [x for x in below if network.edge[x][node]['type'] == 'annotated_by']

    for general_relation, specific_relation in interdependent_relations:
        # this is to take care of compositums of relations, such as part_of and is_a, which compose into part_of.
        # in that context, part of is more general, is_a is more specific.
        relations.remove(general_relation)
        relations.remove(specific_relation)

        general_below = [x for x in below if network.edge[x][node]['type'] == general_relation]
        general_above = [x for x in above if network.edge[x][node]['type'] == general_relation]
        specific_below = [x for x in below if network.edge[x][node]['type'] == specific_relation]
        specific_above = [x for x in above if network.edge[x][node]['type'] == specific_relation]
        for upper in general_above:
            for lower in general_below + specific_below:
                network.add_edge(lower, upper, type=general_relation)
                belows[upper].add(lower)
            belows[upper].remove(node)
        for upper in specific_above:
            for lower in general_below:
                network.add_edge(lower, upper, type=general_relation)
                belows[upper].add(lower)
            for lower in specific_below:
                network.add_edge(lower, upper, type=specific_relation)
                belows[upper].add(lower)
            for example in examples:
                network.add_edge(example, upper, type='annotated_by')
                belows[upper].add(example)
            belows[upper].remove(node)

    for relation in relations:
        r_below = [x for x in below if network.edge[x][node]['type'] == relation]
        r_above = [x for x in above if network.edge[node][x]['type'] == relation]
        for upper in r_above:
            for lower in r_below:
                network.add_edge(lower, upper, type=relation)
                belows[upper].add(lower)
            for example in examples:
                network.add_edge(example, upper, type='annotated_by')
                belows[upper].add(example)
            belows[upper].remove(node)
    network.remove_node(node)


def shrink_hyper_by_pr(network, node_list, pr, percentage, enriched_symbols):
    if percentage < 1:
        new_node_list = []
        for node_index, node in enumerate(node_list):
            if not node.startswith('r_') and not node.startswith('a_') and not network[node].values()[0]['type'] == 'predicate':
                new_node_list.append((node, pr[node_index]))
        new_node_list.sort(key=lambda x: x[1], reverse=True)
        # threshold = new_node_list[int(percentage * len(new_node_list))]
        for node, score in new_node_list[int(percentage * len(new_node_list)):]:
            if node not in enriched_symbols:
                remove_hyper(network, node)
    #         # network.remove_node(node)
    # else:
    #     for node in enriched_symbols:
    #         if node in network:
    #             network.remove_node(node)


def remove_hyper(network, node):
    relations = defaultdict(list)
    annotations = []
    to_delete = []
    for edge in network.edge[node]:
        if edge.startswith('r_'):
            key = [y for y in network.edge[edge] if network.edge[edge][y]['type'] == 'predicate'].pop()
            relations[key].append(edge)
        elif edge.startswith('a_'):
            to_delete.append(edge)
            annotations.append([x for x in network.edge[edge] if network.edge[edge][x]['type'] == 'object'].pop())
    for relation in relations:
        subject_to = []
        object_to = []
        for edge in relations[relation]:
            if network.edge[edge][node]['type'] == 'subject':
                try:
                    subject_to.append([x for x in network.edge[edge] if network.edge[edge][x]['type'] == 'object'].pop())
                except Exception:
                    print("ojoj.")
            elif network.edge[edge][node]['type'] == 'object':
                object_to.append([x for x in network.edge[edge] if network.edge[edge][x]['type'] == 'subject'].pop())
            else:
                raise Exception('This should not happen')
            network.remove_node(edge)
        for object in subject_to:
            for subject in object_to:
                relation_node = 'r_n_%s-%s' % (subject[-7:], object[-7:])
                if relation_node in network:
                    assert object in network.edge[relation_node]
                    assert subject in network.edge[relation_node]
                    assert relation in network.edge[relation_node]
                else:
                    network.add_node(relation_node)
                    network.add_edge(relation_node, object, type='object')
                    network.add_edge(relation_node, subject, type='subject')
                    network.add_edge(relation_node, relation, type='predicate')
            for annotation in annotations:
                annotation_node = 'a_n_%s-%s' % (annotation.split('#')[-1], object[-7:])
                if annotation_node in network:
                    assert object in network.edge[annotation_node]
                    assert annotation in network.edge[annotation_node]
                    assert 'annotates' in network.edge[annotation_node]
                else:
                    network.add_node(annotation_node)
                    network.add_edge(annotation_node, object, type='subject')
                    network.add_edge(annotation_node, annotation, type='object')
                    network.add_edge(annotation_node, 'annotates', type='predicate')
    for x in to_delete:
        network.remove_node(x)
    network.remove_node(node)





def label_propagation_normalization(matrix):
    matrix = matrix.tocsr()
    try:
        matrix.setdiag(0)
    except TypeError:
        matrix.setdiag(np.zeros(matrix.shape[0]))
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    d[nzs] = 1 / np.sqrt(d[nzs])
    dm = sp.diags(d, 0).tocsc()
    return dm.dot(matrix).dot(dm)


def label_propagation(graph_matrix, class_matrix, alpha, epsilon=1e-12, max_steps=10000):
    # This method assumes the label-propagation normalization and a symmetric matrix with no rank sinks.
    steps = 0
    diff = np.inf
    current_labels = class_matrix
    while diff > epsilon and steps < max_steps:
        steps += 1
        new_labels = alpha * graph_matrix.dot(current_labels) + (1 - alpha) * class_matrix
        diff = np.linalg.norm(new_labels - current_labels) / np.linalg.norm(new_labels)
        current_labels = new_labels
    return current_labels
