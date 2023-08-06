from setuptools import setup, find_packages

packages = find_packages()

setup(
    name='microfaune_ai',
    version='1.0.0',
    author="Microfaune - Data For Good",
    author_email="microfaune@fake.com",
    url='https://github.com/microfaune/microfaune_ai',
    description='Module package used for the Microfaune project',
    long_description='Biodiversity evaluation and monitoring is the first step toward its protection. The goal of the Microfaune project is to evaluate avifauna in Cité Internationale park (Paris, France) from audio recordings',
    license='Open license',
    packages=find_packages(),
    package_data={'': ['data/*.h5']}
)
