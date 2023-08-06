import sys
import os

class SimulationInterface():
    """GenericSimulationLibrary is a package encapsulates a methodology 
    and tools for reproducible simulations. 
    The main idea is to use python and/or jupyter notebooks to provide a 
    lightweight and for-dummies easy “Simulation as a Service”. 
    The framework puts emphasis on simplicity: 
    for the client to install and use, 
    for the programmer to distribute and update, 
    and for everyone to store and reproduce results. 
    The framework can be personalized and extended for a specific simulation need.
    Link: https://pypsdier.readthedocs.io/
    """

    def __init__(self):
        """Initializes the class, with no inputs. 
        Will assume that if you have the colab library installed, 
        you're running on google colab(oratory). 

        :return: Nothing
        :rtype: Nothing
        """
        self.configuration = self.__get_configuration()
        self.inputs = {}
        self.plot_options = {}
        self.outputs = {}
        return

    def __get_configuration(self):
        """Carefully tries to import required libraries,
        storing the python and library version.

        :return: Nothing
        :rtype: Nothing
        """
        # Gets the library version
        from .version_file import version_number as GSL_version
        # Gets the python environmnet
        try:
            import colab
            pyenv = "google_colab"
        except:
            try:
                aux = __file__
                pyenv = "python"
            except:
                print("Not in python")
                pyenv = "jupyter_notebook"
        # Check the version for python
        try:
            import platform
            python_version = platform.python_version()
        except:
            python_version = ""
        # Check the version for numpy library
        try:
            from numpy import version as numpy_version
            numpy_version = numpy_version.version
        except:
            numpy_version = ""
        # Check the version for scipy library
        try:
            from scipy import version as scipy_version
            scipy_version = scipy_version.version
        except:
            scipy_version = ""
        # Check the version xlwt library
        try:
            from xlwt import __VERSION__ as xlwt_version
            xlwt_version = xlwt_version
        except:
            xlwt_version = ""
        # Check the version for dill
        try:
            from dill import __version__ as dill_version
        except:
            dill_version = ""
        # Check the version for matplotlib pyplot
        try:
            from matplotlib import __version__ as plt_version
        except:
            plt_version = ""
        # Pack and return
        configuration = {
                         "environment":pyenv,
                         "python_version":python_version,
                         "GenericSimulationLibrary_version":GSL_version,
                         "numpy_version":numpy_version,
                         "scipy_version":scipy_version,
                         "xlwt_version":xlwt_version,
                         "matplotlib_version":plt_version,
                         "dill_version":dill_version,
                         }
        return configuration

    def status(self):
        """Prints out the detected configuration: environment, python and library versions.
        """
        # Configuration
        print("System configuration:")
        for key in self.configuration:
            library = "    " + key.replace("_", " ") + ":"
            if self.configuration[key]:
                print(library, self.configuration[key])
            else:
                print(library, "Not installed")
        # Inputs
        print("Inputs:")
        if self.inputs:
            for key in self.inputs:
                print("    "+key, self.inputs[key])
        else:
            print("    No inputs")
        # plot_options
        print("plot_options:")
        if self.plot_options:
            for key in self.plot_options:
                print("    "+key, self.plot_options[key])
        else:
            print("    No plot_options")
        return  

    def new(self, inputs, plot_options=None):
        """Associates inputs and plot options to the simulation. 

        :param inputs: The inputs that will be used in the simulation. 
            This can be completely personalized. 
        :type inputs: dict
        :param plot_options: The plot options, defaults to None
        :type plot_options: dict, optional
        """
        self.inputs = inputs
        self.plot_options = plot_options
        # Some other computations
        #from IPython import embed; embed()
        ## Compute the expected radius
        E_R = sum([R_i*p_i for R_i, p_i in zip(self.inputs['CatalystParticleRadius'], self.inputs['CatalystParticleRadiusFrequency'])])
        ## Compute the expected value
        from math import pi
        E_V = 4*pi/3 * E_R**3 
        ## Compute the total number of particles
        E_n = self.inputs['BulkVolume'] / E_V
        ## Compute the number of particles for each size
        n_list = []
        for p_i in self.inputs['CatalystParticleRadiusFrequency']:
            n_list.append(E_n * p_i)
        # Setup
        setup = {}
        setup["ExpectedParticleRadius"] = E_R
        setup["ExpectedParticleVolume"] = E_V
        setup["ExpectedParticleNumber"] = E_n
        setup["ParticleNumberByRadius"] = n_list
        return
        
    def save(self, filename):
        """Saves the current state of the simulation, with all
        the provided information. The created file can be
        used with the `load` method to restore the simulation. 

        :param filename: Name for the simulation file.
        :type filename: string
        """
        if not self.configuration["dill_version"]:
            print("Cannot save - dill library not installed.")
            return
        else:
            import dill
        # Pickle and return
        my_dict = {
                   "configuration":self.configuration,
                   "inputs":self.inputs, 
                   "outputs":self.outputs,
                   "plot_options":self.plot_options,
                  }
        filepath = os.path.abspath(filename)
        with open(filename, "wb") as fh:
            dill.dump(my_dict, fh)
            print(f"Saving simulation into file at {filepath}")
        self.download(filename)  #Offer to download the file 
        return

    def load(self, filename):
        """Loads a simulation from a simulation file generated
        with the `save` method to restore the simulation. 

        :param filename: Name for the simulation file.
        :type filename: string
        """
        if not self.configuration["dill_version"]:
            print("Cannot load - dill library not installed.")
            return
        else:
            import dill
        # Unpack and assign
        filepath = os.path.abspath(filename)
        with open(filepath, "rb") as fh:
            my_dict=dill.load(fh)
        self.configuration=my_dict["configuration"]
        self.inputs=my_dict["inputs"] 
        self.outputs=my_dict["outputs"] 
        self.plot_options=my_dict["plot_options"]
        print(f"Loaded a simulation from {filepath}")
        return

    def simulate(self, sim_type):
        """Function that encapsulates the numerical simulation.
        Stores the simulation internally.

        :param sim_typle: Type of simulation required. Only two options: ode or pde.
        :type x_min: string
        :return: Dictionary with the results of the simulation
        :rtype: dict
        """
        # Skip the simulation if numpy not installed
        if not self.configuration["numpy_version"]:
            print("Cannot simulate - numpy library not installed.")
            return
        # Skip the simulation if scipy not installed
        if not self.configuration["scipy_version"]:
            print("Cannot simulate - scipy library not installed.")
            return
        # Simulate accordingly
        if sim_type=="ode":
            from .ode_library import ode_solver
            self.outputs["ode"] = ode_solver(self.inputs)
        elif sim_type=="pde":
            from .pde_library import pde_solver
            self.outputs["pde"] = pde_solver(self.inputs)
        else:
            print("Unknow simulation type. Only ode or pde allowed.")
            outputs = {}
        return
    
    def plot(self, plot_type="all", filename="", display=True):
        """Conditionally imports the matplotlib library,
        and if possible, plots the experimental data given
        in plot_options, and the simulation data.
        
        :param plot_type: ?
        :type plot_type: ?
        :param filename: Filename to save the graph. If not provided, figure is not saved. Defaults to ''.
        :type filename: str, optional
        :param display: Boolean to show (True) or not show (False) the graph. Defaults to False
        :type display: bool, optional
        """
        # Skip the simulation if numpy not installed
        if not self.configuration["matplotlib_version"]:
            print("Cannot simulate - numpy library not installed.")
            return
        # plot
        from .visualization import plot
        plot(self.plot_options, self.inputs, self.outputs)
        """
        if plot_type=="Enzyme":
            from .visualization import plot_E
            T
            E
            plot_E(T, E, self.plot_options)
        elif plot_type=="ode":
            from .visualization import plt_ode
            plot_ode(T, C)
        elif plot_type=="ode":
            from .visualization import plt_pde
            plot_pde(T, C, "")
        elif plot_type=="all":
            from .visualization import plot_ode_and_pde
            plot_ode_and_pde(T, C, "")
        elif plot_type=="particle_pde"
            from .visualization import plot_particle_pde
            plot_particle_pde(T, C, legend)
        else:
            print("Plot type not known.")
        """
        return

    def export_xls(self, filename):
        """Creates an excel file and saves
        the plot data and simulation data.
        It helps providing a file format
        that final users might be more familiar with.        

        :param filename: Name for the file.
        :type filename: string
        """
        if filename[-4:]!=".xls":
            print("Only .xls format allowed.")
            return
        # Create the file
        if self.configuration["xlwt_version"]:
            from .xls_library import save_as_spreadsheet
            save_as_spreadsheet(self.inputs, self.outputs, filename)
            self.download(filename)  #Offer to download the file 
        
    def download(self, filename):
        """Utility to download file, using colab.
        """
        if self.configuration["environment"]=="google_colab":
            from google.colab import files
            files.download(filename)
        return