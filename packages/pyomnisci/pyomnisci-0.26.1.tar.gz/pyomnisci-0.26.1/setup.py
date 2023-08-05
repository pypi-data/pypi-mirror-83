import os
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'pyarrow == 0.17.1',
    'pyomniscidb >=5.4.0',
    'shapely',
    'sqlalchemy >= 1.3',
    'pandas >= 1.1.0,<1.2.0',
    'packaging >= 20.0',
    'requests >= 2.23.0',
    'numba >= 0.48',
]

# Optional Requirements
doc_requires = ['sphinx', 'numpydoc', 'sphinx-rtd-theme']
test_requires = ['coverage', 'pytest', 'pytest-mock', 'geopandas']
dev_requires = doc_requires + test_requires + ['pre-commit']
complete_requires = dev_requires


extra_requires = {
    'docs': doc_requires,
    'test': test_requires,
    'dev': dev_requires,
    'complete': complete_requires,
}

setup(
    name='pyomnisci',
    description='Data science toolkit support for OmniSciDB',
    long_description=long_description,
    url='https://github.com/omnisci/pyomnisci',
    author='OmniSci',
    author_email='community@omnisci.com',
    license='Apache Software License',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
    extras_require=extra_requires,
)
