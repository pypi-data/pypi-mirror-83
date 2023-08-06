from setuptools import setup, find_packages

import numpy as np

setup(name='daproli',
      version='0.22',
      url='https://github.com/ermshaua/daproli',
      license='BSD 3-Clause License',
      author='Arik Ermshaus',
      description='daproli is a small data processing library that attempts to make data transformation more declarative.',
      packages=find_packages(exclude=['tests', 'examples']),
      install_requires=np.loadtxt(fname='requirements.txt', delimiter='\n', dtype=np.str).tolist(),
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      zip_safe=False)
