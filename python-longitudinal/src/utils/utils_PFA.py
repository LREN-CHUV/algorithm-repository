#!/usr/bin/env python3

import logging
import os
#import sys
import math


def get_parameters_from_population_file(path):
    return

def get_parameters_from_individual_file(path):
    return

def get_model_function(type):
    return

# TODO: convert to PFA, with inputs t0 and v0
def get_univariate_function(t, p, v0, t0):
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
    return {"input":
                {
                "type": "record",
                "fields":{
                        {"name": "t", "type": float},
                        {"name": "p", "type": float},
                        {"name": "v0", "type": float},
                        {"name": "t0", "type": float}
                    }
                },
            "output": "float",
            "action":
                {"/":
                    [1,
                    {"+":
                       [1,
                        {"*":
                            [{"+":
                                [{"/":
                                    [1,
                                    {"/":
                                        [1,
                                        {"+":
                                            [1,
                                            {"m.exp": [{"u-": [input.p]}]}]
                                         }]
                                    }] #P0 end
                                },
                                {"u-": [1]}]
                            },
                            {"m.exp":
                                [{"*", [{"u-": [input.v0]},
                                        {"-" : [input.t,
                                                input.t0]}]
                                }]
                            }]
                        }]
                    }]
                }
            }

# TODO: convert to PFA, with inputs t0 and v0
def get_multivariate_function(t, g, delta, w, v0, t0):
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
    return {"input":
                {
                "type": "record",
                "fields":{
                        {"name": "t", "type": float},
                        {"name": "g", "type": float},
                        {"name": "w", "type": float},
                        {"name": "v0", "type": float},
                        {"name": "t0", "type": float},
                        {"name": "delta", "type": float}
                    }
                },
            "output": "float",
            "action":
                { "/",
                    [1,
                    {"+",
                        [1,
                        {"*",
                            [input.g,
                            {"m.exp",
                                [{"+",
                                    [{"*",
                                        [{"*",
                                            [{"u-", [input.w]},
                                             {"m.exp", [{"u-", [input.delta]}]}]
                                          },
                                        {"/",
                                            [{"**",
                                                [{"+",
                                                    [{"*", [input.g,
                                                            {"m.exp", [{"u-", [input.delta]}]}]
                                                      },
                                                      1]
                                                  },
                                                  2]
                                              },
                                              input.g]
                                        }]
                                    },
                                    {"+",
                                        [{"u-", [input.delta]},
                                         {"*",
                                            [{"u-", [input.v0]},
                                             {"-", [input.t, input.t0]}]
                                         }]
                                    }]
                                }]
                            }]
                        }]
                    }]
                }
            }

def write_output_to_pfa(model_type):
    #reads the population file
    #creates the pfa file
    #creates the dict for the population
    #creates the dict for the individuals
    return