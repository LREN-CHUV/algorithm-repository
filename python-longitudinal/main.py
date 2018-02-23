#!/usr/bin/env python3

import logging
import os

try:
    from io_helper import io_helper
except:
    print("No import")

try:
    import utils_write_input
except:
    from utils import utils_write_input

try:
    import utils
except:
    from utils import utils


def main():
    logging.basicConfig(level=logging.INFO)
#    try:
#        data = io_helper.fetch_data() #renverra des dataframes pandas => 2 novembre, envoyer message to Mirco
#        model_type = utils_write_inputs.write_input_to_file(data)
#    except:
#        model_type = "univariate"

    model_type = "univariate"

    os.system("./main_" + model_type + ".sh")
    highchart = utils.write_output_to_highchart(model_type)
    pfa = utils.write_output_to_pfa(model_type)

    io_helper.save_results(highchart, "icm_algo", "highcharts_json")





if __name__ == '__main__':
    main()
