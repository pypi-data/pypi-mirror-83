from setuptools import setup
from codecs import open
from os import path, walk

here = path.abspath(path.dirname(__file__))

__version__ = ""
exec(open("./pytle/version.py").read())

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytle',
    version=__version__,

    description='Simple utility and module to download and load TLE information',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/jeremymturner/pytle',

    author='Jeremy Turner',
    author_email='jeremy@jeremymturner.com',

    # Choose your license
    license='Apache',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # What does your project relate to?
    keywords='hamradio satellites tle',

    packages=['pytle'],

    include_package_data=True,

    install_requires=['ephem','jinja2'],

    entry_points={
        'console_scripts': [
            'pytle=pytle.cli:main',
        ],
    },
)
