#!/usr/bin/env python3

#import sys
try:
    import utils_highcharts
except:
    from utils import utils_highcharts

def write_output_to_highchart(model_type):
    if model_type == "univariate":
        return utils_highcharts.write_univar_output_to_highchart()
    if model_type == "multivariate":
        return utils_highcharts.write_multivar_output_to_highchart()

# Might need to add a transformation function to go from the dictionnary to lists to write in the different files,
# especially if we get several queries.
def write_input_to_file(data):
    path_to_group_file = "longitudina/examples/scalar_models/univariate/sigmoid/data/groups.csv"
    path_to_X_file = "longitudina/examples/scalar_models/univariate/sigmoid/data/X.csv"
    path_to_Y_file = "longitudina/examples/scalar_models/univariate/sigmoid/data/Y.csv"

    data_stores = data["data"]["independent"]
    dimension = 1
    for item_dict in data_stores:
        if item_dict["name"] == "id":
            write_content_to_file(item_dict["series"], path_to_group_file)
        if item_dict["name"] == "age":
            write_content_to_file(item_dict["series"], path_to_X_file)
        if item_dict["name"] == "scores":
            write_content_to_file(item_dict["series"], path_to_Y_file)
            dimension = item_dict["series"].size()

    model_type = edit_settings_files(dimension)

    return model_type

# If needed, edit this function to use several series (for multivariate).
def write_content_to_file(serie, path_to_file):
    file = open(path_to_file, "w+")
    for value in serie:
        file.write(value)
    file.close()

# This function must edit the settings file to take into account the number of scores (the dimension)
# and return the model_type
def edit_settings_files(dimension):
    # write dimension in xml

    model_type = ""
    if dimension == 1:
        model_type = "univariate"
    elif dimension > 1:
        model_type = "multivariate"
    return model_type