from .library import cf_netsdm_reduce, cf_load_gml, cf_hinmine_decompose_post, \
    cf_hinmine_propositionalize, cf_hinmine_label_propagation


def netsdm_reduce(examples, bk_file, target, directed, minimum_ranking, hyper, adv_removal):
    return cf_netsdm_reduce({'examples': examples,
                             'bk_file': bk_file,
                             'target': target,
                             'adv_removal': 'true' if adv_removal else 'false',
                             'directed': 'true' if directed else 'false',
                             'minimum_ranking': minimum_ranking,
                             'hyper': 'true' if hyper else 'false',
                             'interdependent_relations': [('http://kt.ijs.si/jan_rel#part_of', 'http://kt.ijs.si/jan_rel#is_a')]}) #TODO: improve this!!!


def load_gml(file, label_delimiter):
    return cf_load_gml({'file': file,
                        'label_delimiter': label_delimiter})['net']


def hinmine_decompose(network, heuristic, cycle=None):
    if cycle is None:
        candidates = network.calculate_decomposition_candidates()
        raise Exception('No decomposition cycle provided. Candidate cycles are: %s' % candidates)
    return cf_hinmine_decompose_post({'cycle': cycle},
                                     {'network': network,
                                      'heuristic': heuristic},
                                     {})['network']


def hinmine_propositionalize(network, damping):
    return cf_hinmine_propositionalize({'network': network, 'damping': damping})


def hinmine_label_propagation(network, weights=None, alpha=0.85, semibalanced=None):
    return cf_hinmine_label_propagation({'network': network})['result']
