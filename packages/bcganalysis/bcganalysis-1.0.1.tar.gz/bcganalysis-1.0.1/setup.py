# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='bcganalysis',
    version='1.0.1',
    author='Matias Eiletz',
    author_email='mat.eil1991@gmail.com',
    description='Builds BCG Matrix',
    keywords='BCG Growth Share Matrix Feature Importance Clustering',
    packages = ['bcg_analysis'],
    url='https://github.com/mateil04/bcg_analysis',
	zip_safe=False
)