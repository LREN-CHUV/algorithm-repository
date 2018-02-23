from django.shortcuts import render


def cf_hinmine_decompose_interact(request, input_dict, output_dict, widget):
    network = input_dict['network']
    cycles = network.calculate_decomposition_candidates()
    input_dict['cycles'] = cycles
    view_cycles = []
    for cycle in cycles:

        view_cycles.append({
            'nice_value': '-->'.join(['-->'.join(x) for x in zip(cycle['node_list'], cycle['edge_list'] + [''])])[:-3],
            'value': '_____'.join(['_____'.join(x) for x in zip(cycle['node_list'], cycle['edge_list'] + [''])])[:-5]
        })
    output_dict['test'] = 'test'
    return render(request,
                  'interactions/hinmine_decompose_interact.html',
                  {'widget': widget, 'cycles': view_cycles})
