import networkx as nx
from .settings import HEDWIG
from rdflib import RDF
from rdflib.term import Literal
from .helpers import user_defined, prepare
import logging
import rdflib
from collections import defaultdict


def n3_to_nx(data, positive_class):
    return_graph = nx.DiGraph()
    return_non_targets = defaultdict(list)
    positive_class = Literal(positive_class)
    generelization_predicates = list(data.subjects(predicate=RDF.type, object=HEDWIG.GeneralizationPredicate))
    for predicate in generelization_predicates:
        for sub, obj in data.subject_objects(predicate=predicate):
            if user_defined(sub) and user_defined(obj):
                return_graph.add_edge(sub, obj, type=predicate)
    target_nodes = set()
    bad_annotations = []
    for example in data.subjects(predicate=RDF.type, object=HEDWIG.Example):
        positive = (example, HEDWIG.class_label, positive_class) in data
        if positive:
            target_nodes.add(example)
        for annotation_link in data.objects(subject=example, predicate=HEDWIG.annotated_with):
            annotations = data.objects(subject=annotation_link, predicate=HEDWIG.annotation)
            annotation = annotations.next()
            if next(annotations, None) is not None:
                raise Exception("Unable to parse data - annotations for example %s are unclear" % example)
            if annotation not in return_graph:
                bad_annotations.append(annotation)
                #raise Exception("Data - BK synchronization error: annotation %s does not appear in the Background "
                #                "knowledge!" % annotation)
            if positive:
                return_graph.add_edge(example, annotation, type='annotated_by')
            else:
                return_non_targets[example].append(annotation)
    if len(bad_annotations) > 0:
        bad_annotations = set(bad_annotations)
        raise Exception("%i bad annotations detected: " % len(bad_annotations) + ', '.join(list(bad_annotations)))
    roots = [node for node in return_graph if len(return_graph.edge[node]) == 0]
    for root in roots:
        return_graph.add_edge(root, HEDWIG.dummy_root, type=RDF.type)
    return return_graph, target_nodes, return_non_targets, generelization_predicates



def nx_to_n3(network, positive_nodes, n):
    logging.info('Building graph')
    p = set(positive_nodes)
    pun = p.union(n)
    ns1 = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    ontology = rdflib.Graph()
    annotations = rdflib.Graph()
    for term in network.node:
        if term in pun:
            annotations.add((term, rdflib.RDF.type, ns1.Example))
            for end in network.edge[term]:
                blank = rdflib.BNode()
                annotations.add((term, ns1.annotated_with, blank))
                annotations.add((blank, ns1.annotation, end))
            if term in p:
                annotations.add((term, ns1.class_label, rdflib.Literal('+')))
            elif term in n:
                annotations.add((term, ns1.class_label, rdflib.Literal('-')))
            else:
                raise Exception('Unexpected data set error.')
        else:
            for end in network.edge[term]:
                if end not in pun:
                    ontology.add((term, network.edge[term][end]['type'], end))
    return ontology, annotations


def n3_to_nx_hyper(data, positive_class):
    return_non_targets = defaultdict(list)
    return_graph = nx.Graph()
    positive_class = Literal(positive_class)
    generelization_predicates = list(data.subjects(predicate=RDF.type, object=HEDWIG.GeneralizationPredicate))
    for predicate in generelization_predicates:
        for sub, obj in data.subject_objects(predicate=predicate):
            if user_defined(sub) and user_defined(obj):
                relation_node = 'r_%s-%s' % (sub[-7:], obj[-7:])
                assert relation_node not in return_graph
                return_graph.add_node(relation_node)
                return_graph.add_edge(relation_node, sub, type='subject')
                return_graph.add_edge(relation_node, obj, type='object')
                return_graph.add_edge(relation_node, predicate, type='predicate')
                x = 1

    target_nodes = set()
    i = 0
    for example in data.subjects(predicate=RDF.type, object=HEDWIG.Example):
        if (example, HEDWIG.class_label, positive_class) in data:
            target_nodes.add(example)
            for annotation_link in data.objects(subject=example, predicate=HEDWIG.annotated_with):
                annotations = data.objects(subject=annotation_link, predicate=HEDWIG.annotation)
                annotation = annotations.next()
                if next(annotations, None) is not None:
                    raise Exception("Unable to parse data - annotations for example %s are unclear" % example)
                if annotation not in return_graph:
                    raise Exception("Data - BK synchronization error: annotation %s does not appear in the Background "
                                    "knowledge!" % annotation)
                # VERSION 1:
                annotation_node = 'a_%s-%s' % (example[-7:], annotation[-7:])
                assert annotation_node not in return_graph
                return_graph.add_node(annotation_node)
                return_graph.add_edge(annotation_node, example, type='object')
                return_graph.add_edge(annotation_node, annotation, type='subject')
                return_graph.add_edge(annotation_node, 'annotates', type='predicate')
                i += 1
                # VERSION 2:
                # return_graph.add_edge(example, annotation)
        else:
            for annotation_link in data.objects(subject=example, predicate=HEDWIG.annotated_with):
                annotations = data.objects(subject=annotation_link, predicate=HEDWIG.annotation)
                annotation = annotations.next()
                if next(annotations, None) is not None:
                    raise Exception("Unable to parse data - annotations for example %s are unclear" % example)
                if annotation not in return_graph:
                    raise Exception("Data - BK synchronization error: annotation %s does not appear in the Background "
                                    "knowledge!" % annotation)
                return_non_targets[example].append(annotation)
    return return_graph, target_nodes, return_non_targets, generelization_predicates


def nx_to_n3_hyper(network, positive_nodes, negative_nodes):
    ns1 = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    p = set(positive_nodes)
    ontology = rdflib.Graph()
    annotations = rdflib.Graph()

    for node in network:
        if node.startswith('r_'):
            assert len(network.edge[node]) == 3
            subject, predicate, object = None, None, None
            for x in network.edge[node]:
                if network.edge[node][x]['type'] == 'subject':
                    subject = x
                elif network.edge[node][x]['type'] == 'object':
                    object = x
                elif network.edge[node][x]['type'] == 'predicate':
                    predicate = x
                else:
                    raise Exception('This should not happen')
            if subject is None or predicate is None or object is None:
                raise Exception('This should not happen')
            ontology.add((subject, predicate, object))
        if node.startswith('a_'):
            blank = rdflib.BNode()
            for end in network.edge[node]:
                if network.edge[node][end]['type'] == 'subject':
                    annotations.add((blank, ns1.annotation, end))
                elif network.edge[node][end]['type'] == 'object':
                    annotations.add((end, ns1.annotated_with, blank))
                    annotations.add((end, rdflib.RDF.type, ns1.Example))
                    if end in p:
                        annotations.add((end, ns1.class_label, rdflib.Literal('+')))
                    else:
                        annotations.add((end, ns1.class_label, rdflib.Literal('-')))
    return ontology, annotations


def digraph_to_graph(graph):
    return nx.Graph(graph)

ALEPH_SETTINGS = {
    'caching': 'true',
    'noise': '200',
    'search': 'heuristic',
    'evalfn': 'wracc',
    'minposfrac': '0.01'
}


def convert_to_aleph(input_dict):
    return_dict = {'background': ''}
    data = rdflib.Graph()
    prepare(data)
    print("parsing examples")
    data.parse(data=input_dict['examples'], format='n3')
    print("parsing bk")
    for ontology in input_dict['bk_file']:
        data.parse(data=ontology, format='n3')
    settings = input_dict['settings'] if 'settings' in input_dict else ALEPH_SETTINGS
    generalizations = defaultdict(list)
    annotations = defaultdict(list)
    print("going through generalization predicates")
    generelization_predicates = list(data.subjects(predicate=RDF.type, object=HEDWIG.GeneralizationPredicate))
    for predicate in generelization_predicates:
        for sub, obj in data.subject_objects(predicate=predicate):
            if user_defined(sub) and user_defined(obj):
                generalizations[sub].append(obj)
    print("going through examples")
    pos = ''
    neg = ''
    positive_class = Literal(input_dict['positive_class'])
    for example in data.subjects(predicate=RDF.type, object=HEDWIG.Example):
        positive = (example, HEDWIG.class_label, positive_class) in data

        if positive:
            pos += 'positive(\'%s\').\n' % example
        else:
            neg += 'positive(\'%s\').\n' % example
        for annotation_link in data.objects(subject=example, predicate=HEDWIG.annotated_with):
            example_annotations = data.objects(subject=annotation_link, predicate=HEDWIG.annotation)
            annotation = example_annotations.next()
            if next(example_annotations, None) is not None:
                raise Exception("Unable to parse data - annotations for example %s are unclear" % example)
            annotations[example].append(annotation)
    print("writing bk")
    bk = ':- modeh(1, positive(+instance)).\n'
    bk += ':- mode(*, annotated_with(+instance, #annotation)).\n'
    bk += ':- determination(positive/1, annotated_with/2).\n'
    bk += '\n\n'
    for setting in settings:
        bk += ':- set(%s, %s).\n' % (setting, settings[setting])
    bk += '\n\n'

    for sub_concept in generalizations:
        for super_concept in generalizations[sub_concept]:
            bk += 'annotated_with(X, \'%s\') :- annotated_with(X, \'%s\').\n' % (super_concept, sub_concept)
    bk += '\n'
    print("writing pos and neg")
    i = 0
    print(len(annotations))
    for example in annotations:
        i += 1
        if i%1000 == 0:
            print(i)
        for concept in annotations[example]:
            bk += 'annotated_with(\'%s\', \'%s\').\n' % (example, concept)
    return_dict['bk'] = bk
    return_dict['pos'] = pos
    return_dict['neg'] = neg
    print("done!!!")
    return return_dict
