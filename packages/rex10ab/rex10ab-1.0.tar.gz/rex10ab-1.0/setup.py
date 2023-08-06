from setuptools import setup, find_packages

setup(
    name='rex10ab',
    version='1.0',
    description='read smv file, write hdf file, etc.',
    author='Rui Xu',
    author_email='rickxu2020@gmail.com',
    packages=find_packages(),
    install_requires=['numpy','h5py','pyfftw']
)