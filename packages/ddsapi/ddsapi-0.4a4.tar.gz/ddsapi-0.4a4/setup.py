"""Packaging utility for CMCC DDSAPI"""


# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/discussions/install-requires-vs-requirements/
# https://pypi.org/classifiers/
# https://setuptools.readthedocs.io/en/latest/setuptools.html

# Run this file with the command:
# $ python setup.py install


import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ddsapi',
    version='0.4a4',
    author='PPOS Research Group',
    author_email='ppos-services@cmcc.it',
    description=('Python Client to access and download data from CMCC Data Delivery System (DDS)'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=('https://github.com/CMCC-Foundation/ddsapi-client/'
         'ddsapi/ddsapi'),
    packages=setuptools.find_packages(),
    install_requires=[
        'netCDF4>=1.5.3',
        'scipy>=1.5.2',
        'requests>=2.23.0',
        'xarray==0.16.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Hydrology'
    ],
    python_requires='>=3.7',
    license='Apache License, Version 2.0'
)
