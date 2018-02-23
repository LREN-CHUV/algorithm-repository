from scipy import stats
import logging


def binarize(att, values, bins, target=False):
    _, edges, membership = stats.binned_statistic(values, values, bins=bins)

    binned_attributes = {}
    if target:
        # For the target attribute, use the bins as target values
        target_values = []
        for i, _ in enumerate(edges):
            lower, upper = str(edges[i]), str(edges[(i + 1) % len(edges)])
            target_values.append('{}<={}<{}'.format(lower, att, upper))

        binned_attributes[att] = []
        for j, bin_idx in enumerate(membership):
            binned_attributes[att].append(target_values[bin_idx - 1])
    else:
        for i in range(1, len(edges)):
            lower, upper = str(edges[i - 1]), str(edges[i])
            binned_attributes['{}<={}<{}'.format(lower, att, upper)] = []

        for i, new_att in enumerate(binned_attributes):
            binned_attributes[new_att] = []
            for j, bin_idx in enumerate(membership):
                binned_attributes[new_att].append('0' if bin_idx - 1 != i else '1')

    return binned_attributes


def preprocess_attribute(att, series_map, bins, target=False):
    name = att['name']
    series = att['series']
    type = att['type']['name']

    # Check if binarization is needed
    if type == 'real':
        binned_attributes = binarize(name, series, bins, target=target)
        for att in binned_attributes:
            series_map[att] = binned_attributes[att]
    else:
        series_map[name] = series


def to_matrix(data, do_binarize=True, bins=4):
    ''' Converts the input json data to a data list, a list of attributes and types '''
    series_map = {}

    if len(data['dependent']) > 1:
        logging.warning('Multiple dependent vars detected: selecting the first one.')

    target_att = data['dependent'][0]
    target_att_name = target_att['name']
    preprocess_attribute(target_att, series_map, bins, target=True)

    for att in data['independent']:
        preprocess_attribute(att, series_map, bins, target=False)

    attributes = list(filter(lambda att: att != target_att_name, series_map.keys())) + [target_att_name]
    n_examples = len(series_map[attributes[-1]])

    data_list = []
    for idx in range(n_examples):
        example = []
        for att in attributes:
            example.append(series_map[att][idx])
        data_list.append(example)

    return data_list, attributes


def dump_to_csv(data, attributes, out_file):
    ''' Output to csv for hedwig '''
    with open(out_file, 'w') as f:
        f.write('{}\n'.format(';'.join(['id'] + attributes)))

        for id, example in enumerate(data):
            f.write('{}\n'.format(';'.join([str(id)] + example)))
