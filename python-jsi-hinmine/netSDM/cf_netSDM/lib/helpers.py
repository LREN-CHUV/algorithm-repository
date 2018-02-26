from .settings import EXAMPLE_SCHEMA, HEDWIG, W3C
from rdflib import RDF


def prepare(data):
    data.parse(EXAMPLE_SCHEMA, format='n3')


def add_generalization_predicates(rdf_network, generalization_predicates):
    for predicate in generalization_predicates:
        rdf_network.add((predicate, RDF.type, HEDWIG.GeneralizationPredicate))


def add_negatives_hyper(network, negatives):
    i = 0
    for negative in negatives:
        for annotation in negatives[negative]:
            annotation_node = 'a_neg_%i' % i
            network.add_node(annotation_node)
            network.add_edge(annotation_node, negative, type='object')
            network.add_edge(annotation_node, annotation, type='subject')
            network.add_edge(annotation_node, 'annotates', type='predicate')
            i += 1

def add_negatives_regular(network, negatives):
    for negative in negatives:
        for annotation in negatives[negative]:
            network.add_edge(negative, annotation, type='annotated_by')


def anonymous_uri(uri):
    return not uri.startswith('http')


def user_defined(uri):
    """
    Is this resource user defined?
    """
    return not uri.startswith(W3C) and not uri.startswith(HEDWIG) and not anonymous_uri(uri)
