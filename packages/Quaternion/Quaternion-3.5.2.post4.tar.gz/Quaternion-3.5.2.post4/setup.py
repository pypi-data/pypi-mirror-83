# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup

try:
    from testr.setup_helper import cmdclass
except ImportError:
    cmdclass = {}


long_description = """Quaternion provides a class for manipulating quaternion objects.

To install:

```
pip install quaternion
```

To run some tests:

```
pip install pytest
python -c 'import Quaternion; Quaternion.test()'
```

Documentation: https://sot.github.io/Quaternion

Source: https://github.com/sot/Quaternion
"""

setup(name='Quaternion',
      author='Jean Connelly',
      description='Quaternion object manipulation',
      long_description_content_type='text/markdown',
      long_description=long_description,
      author_email='jconnelly@cfa.harvard.edu',
      packages=['Quaternion', 'Quaternion.tests'],
      license="New BSD/3-clause BSD License. Copyright (c) 2016 Smithsonian Astrophysical Observatory. All rights reserved.",
      download_url='http://pypi.python.org/pypi/Quaternion/',
      url='https://sot.github.io/Quaternion',
      version='3.5.2.post4',
      zip_safe=False,
      tests_require=['pytest'],
      package_data={'Quaternion.tests': ['data/*.pkl']},
      cmdclass=cmdclass,
      install_requires=[
          'numpy',
      ],
      )
