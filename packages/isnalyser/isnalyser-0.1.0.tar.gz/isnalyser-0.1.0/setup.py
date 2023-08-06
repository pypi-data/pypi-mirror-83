import setuptools
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name='isnalyser', # what people pip install
	version='0.1.0', # version of our library
	description='Create isnad graphs automatically.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	python_requires=">=3.5", # python version
	install_requires= ["pandas>=0.24.2", "graphviz>=0.11.1", "matplotlib>=2.0.0", "numpy>=1.12.0"], # dependencies and their versions
	url='https://github.com/dhakara/isnalyser',
	author='Maroussia Bednarkiewicz, Stefan Wezel, Álvaro Tejero Cantero',
	author_email='maroussia.b@gmail.com',
	include_package_data=True,
	package_data = {
	'' : ['*.csv']}
	)
	