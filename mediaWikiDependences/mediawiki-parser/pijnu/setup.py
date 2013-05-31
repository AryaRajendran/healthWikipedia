# -*- coding: utf8 -*-
#!/usr/bin/env python

'''
© 2009 Denis Derman (former developer) <denis.spir@gmail.com>
© 2011 Peter Potrowl (current developer) <peter017@gmail.com>

This file is part of PIJNU.

PIJNU is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PIJNU is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PIJNU: see the file called 'GPL'.
If not, see <http://www.gnu.org/licenses/>.
'''


from distutils.core import setup
from datetime import date

long_description = """\
'pijnu' is
* a parsing language extended from PEG,
* a parser generator for grammars written using this language,
* a tool to help processing processing parse results.

'pijnu' is intended to be clear, easy, practical.
"""

# version code should be overloaded by makeRelease
version = 20110610
if version is None:
    version = str(date.today()).replace("-", "")  # eg "20090831"

setup(name="pijnu",
      version=version,
      author="Denis Derman",
      author_email="denis.spir@gmail.com",
      maintainer="Peter Potrowl",
      maintainer_email="peter017@gmail.com",
      url="http://www.github.com/peter17/pijnu",
      license="GPL3",
      platforms=["Any"],
      packages=["pijnu"],
      scripts=[],
      description="text parsing & processing tool",
      long_description=long_description,
      classifiers=[
          'License :: GPL',
          'Development Status :: 4 - Beta',
          'Topic :: Software Development',
          'Topic :: Text Processing',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          ]
      )
