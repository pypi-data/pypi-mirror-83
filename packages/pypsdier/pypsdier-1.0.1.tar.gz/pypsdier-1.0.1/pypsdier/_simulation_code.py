import numpy as np
import time
import sys

def execute_simulation(sim_type, inputs):
    """Function that encapsulates the numerical simulation.

    :param sim_typle: Type of simulation required. Only two options: ode or pde.
    :type x_min: string
    :return: Dictionary with the results of the simulation
    :rtype: dict
    """
    if sim_type=="ode":
        from .ode_library import ode_solver
        outputs = ode_solver(inputs)
    elif sim_type=="pde":
        from .pde_library import pde_solver
        outputs = pde_solver(inputs)
    else:
        print("Unknown simulation type. Only ode or pde allowed.")
        outputs = {}
    return outputs