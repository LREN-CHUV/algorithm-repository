
def read_population_parameters(path_to_file):
    """
    Reads the population parameters file
    Args:
        path_to_file: the path to the population file Longitudina outputted

    Returns:
        dict: a dictionnary with the name of the parameters as keys and their values as values
    """
    reader = csv.reader(open(path_to_file, 'r'))
    params = {}
    params_delta = {}
    params_delta_tilde = {}
    nb_delta = 0
    for row in reader:
        name = row[0].lower()
        if name[0:6] == "delta#":
            params_delta[name] = float(row[1])
            nb_delta += 1
        elif name[0:6] == "delta_":
            params_delta_tilde[name] = float(row[1])
        else:
            params[name] = float(row[1])

    params["deltas"] = [params_delta["delta#"+str(i)] for i in range(len(params_delta))]
    #params["deltas_tilde"] = [params_delta_tilde["delta_tilde#"+str(i)] for i in range(len(params_delta))]

    return params


def read_multiple_individual_parameters(file_name):
    reader = csv.reader(open(file_name, 'r'))
    parameters = {}
    s_parameters_mean = {}
    s_parameters_last = {}

    for row in reader:
        id_ = row[0].strip()
        parameter = row[1].strip().lower()
        last_value = float(row[2].strip())
        mean_value = float(row[3].strip())

        if id_ not in parameters:
            parameters[id_] = {}
            s_parameters_last[id_] = {}
            s_parameters_mean[id_] = {}

        ### Handle the sources
        if parameter[0:2] != "s#":
            parameters[id_]['last_'+parameter] = last_value
            parameters[id_]['mean_'+parameter] = mean_value
        else:
            s_parameters_last[id_][parameter] = last_value
            s_parameters_mean[id_][parameter] = mean_value

    for k, v in s_parameters_last.items():
        values = [v["s#"+str(i)] for i in range(len(v))]
        parameters[k]["last_s"] = values

    for k, v in s_parameters_mean.items():
        values = [v["s#"+str(i)] for i in range(len(v))]
        parameters[k]["mean_s"] = values

    return parameters

def compute_individual_parameters(list_elements, number_of_params):
    """ Reads the individual parameters file
    Args:
        list_elements: the list of the lines extracted from the files
        number_of_params: the number of parameters per trajectory

    Returns:
        dict: dictionnary of individual parameters
    """
    individual_parameters = {}
    idx_start = 0

    for tpl in number_of_params:
        idx_end = idx_start + tpl[1]
        if tpl[0] == "id":
            individual_parameters[tpl[0].rstrip()] = [(list_elements[i].rstrip()) for i in range(idx_start, idx_end)]
        else:
            individual_parameters[tpl[0].rstrip()] = [float(list_elements[i].rstrip()) for i in range(idx_start, idx_end)]
        idx_start = idx_end

    return individual_parameters

