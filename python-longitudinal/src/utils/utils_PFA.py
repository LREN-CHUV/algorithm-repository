#!/usr/bin/env python3

try:
    import utils_read_inputs
except:
    from utils import utils_read_inputs

def get_univariate_function(p, v0, t0):
    """
    Univariate function
    Args:
        t (float): Timescore (equivalent to x)
        p (float):
        v0 (float): acceleration of the slope (individual parameter)
        t0 (float): initial start of the slope for the specific individual (individual parameter)
        p0 = 1/(1 + math.exp(-p))
        result = 1/(1+(1/p0 - 1)*math.exp(-v0*(t-t0)))
    """
    return "{'input': 'double', \
            'output': 'float', \
            'action': \
                {'/': \
                    [1, \
                    {'+': \
                       [1, \
                        {'*': \
                             [{'+': \
                                  [{'/': \
                                      [1, \
                                     {'/': \
                                         [1, \
                                         {'+': \
                                             [1, \
                                             {'m.exp': [{'u-': [" + p + "]}]}] \
                                         }] \
                                    }] #P0 end \
                                }, \
                                {'u-': [1]}]\
                            },\
                            {'m.exp': \
                                 [{'*', [{'u-': [" + v0 + "]}, \
                                        {'-' : [input, \
                                                " + t0 + "]}] \
                                  }]\
                            }]\
                        }]\
                    }]\
                }\
            }"


def get_multivariate_function(g, delta, w, v0, t0):
    """
    Multivariate function
    Args:
        t (float): Timescore (equivalent to x)
        g (float)
        delta (float):
        w (float): weight
        v0 (float): acceleration of the slope (individual parameter)
        t0 (float): initial start of the slope for the specific individual (individual parameter)
        equation: 1 / (1 + g*math.exp ((-w*math.pow(g*math.exp(-delta)+1,2)/g*math.exp(-delta)) - delta - v0*(t - t0)) )
        """

    return "{'input': double, \
             'output': float, \
             'action': \
                { '/', \
                  [1, \
                   {'+', \
                    [1, \
                     {'*', \
                      [" + g + ", \
                       {'m.exp', \
                        [{'+', \
                          [{'*', \
                            [{'*', \
                              [{'u-', [" + w + "]}, \
                               {'m.exp', [{'u-', [" + delta + "]}]}] \
                              }, \
                             {'/', \
                              [{'**', \
                                [{'+', \
                                  [{'*', [" + g + ", \
                                          {'m.exp', [{'u-', [" + delta + "]}]}] \
                                    }, \
                                   1] \
                                  }, \
                                 2] \
                                }, \
                               " + g + "] \
                              }] \
                            }, \
                           {'+', \
                            [{'u-', [" + delta + "]}, \
                             {'*', \
                              [{'u-', [" + v0 + "]}, \
                               {'-', [input," + t0 + "]}] \
                              }] \
                            }] \
                          }] \
                        }] \
                      }] \
                    }] \
                  } \
                }"

def write_output_to_pfa(model_type):
    pop_param = utils_read_inputs.read_population_parameters("longitudina/examples/scalar_models/" + model_type + "/output/population_parameters.csv")
    result_pfa = ""
    if model_type == "univariate":
        result_pfa += get_univariate_function(pop_param['p'], pop_param['v0'], pop_param['t0'])
    elif model_type == "multivariate":
        for delta in pop_param['deltas']:
            result_pfa += get_multivariate_function(pop_param['g'], delta, pop_param['w'], pop_param['v0'], pop_param['t0'])

    return result_pfa
