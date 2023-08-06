# Python Module for Importing Keplerian Elements

By: Jeremy Turner / N0AW <jeremy@jeremymturner.com>

# Quick Installation
`pip install pytle`


# Upgrading
`pip install --upgrade pytle`


# Quick Usage
`pytle --satname SO-50`


# Full Usage
```
usage: pysatadif [-h] -s SATNAME [SATNAME ... ] [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SATNAME, --satname SATNAME [SATNAME ... ]
                        Satellites to track
  -o OUTPUT, --output OUTPUT
                        Output Format (text, json)
  -v, --verbose         Print verbose debugging messages
```

# History

0.0.3 - Removed Python 2 support. fixed json output to be actually json

0.0.2 - Fixed a module name error

0.0.1 - Initial import
