"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Michael Dowd",
    author_email="mikdowd@gmail.com",
    name='datatools-mikdowd',
    license="MIT",
    description='datatools is a python package for doing basic data summaries and other tasks',
    version='v0.0.4',
    long_description=README,
    url='https://github.com/mdgis/datatools',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['pandas', 'seaborn'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)