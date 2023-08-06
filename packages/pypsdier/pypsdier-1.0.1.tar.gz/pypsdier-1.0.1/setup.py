# Library to configure this setup file
from distutils.core import setup

# Import the version of the the pypsdier
from pypsdier import version as current_version
print("Current Library Version:", current_version)

# Use the README for the long description
long_description=open('README.rst').read() ### Change the content of README.rst

setup(
    name='pypsdier',        ### Change here
    version=current_version,
    author='Sebastian Flores Benner',       ### Change here
    author_email='sebastiandres@gmail.com', ### Change here
    packages=['pypsdier'],  ### Change here
    scripts=[],
    url='https://github.com/sebastiandres/pypsdier',    ### Change here
    license='MIT',  ### May/May not change this. But if you change it, must also change LICENCE file
    description='Pythonistic reaction diffusion equation solver.', ### Change here
    long_description=long_description,
)
