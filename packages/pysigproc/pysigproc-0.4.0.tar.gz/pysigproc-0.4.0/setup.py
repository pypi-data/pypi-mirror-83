#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='pysigproc',
      version='0.4.0',
      description='Python reader/writer for sigproc filterbank files.',
      author='Paul Demorest, Devansh Agarwal, Kshitij Aggarwal',
      author_email='pdemores@nrao.edu, da0017@mix.wvu.edu, ka0064@mix.wvu.edu',
      url='http://github.com/devanshkv/pysigproc',
      install_requires=required,
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      py_modules={'pysigproc', 'candidate', 'gpu_utils'},
      scripts=['bin/h5plotter.py'],
      classifiers=[
          'Natural Language :: English',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Topic :: Scientific/Engineering :: Astronomy']
      )
