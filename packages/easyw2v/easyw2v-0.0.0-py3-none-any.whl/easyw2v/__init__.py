"""
easyw2v - Word2Vec from Terminal
=====================================================

*easyw2v* helps to generate semantic (word) vectors for words in a corpus. You do not have to write your own python code, and instead you can generate semantic vectors simply in Terminal with this package.

"""

import os
import sys
import multiprocessing as mp
from pip._vendor import pkg_resources

__author__ = 'Motoki Saito'
__author_email__ = 'motoki.saito@uni-tuebingen.de'
__version__ = '0.0.0'
__license__ = 'MIT'
__description__ = 'Easy generation of semantic vectors from a corpus in Terminal'
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering'
]


def sysinfo():
    """
    Prints the system information
    """
    easyw2v = pkg_resources.working_set.by_key['easyw2v']
    dependencies = [ i.project_name for i in easyw2v.requires() ]

    header = ('Easyw2v Information\n'
              '=================\n\n')

    general = ('General Information\n'
               '-------------------\n'
               'Python version: {}\n'
               'Easyw2v version: {}\n\n').format(sys.version.split()[0], __version__)

    uname = os.uname()
    osinfo = ('Operating System\n'
              '----------------\n'
              'OS: {s.sysname} {s.machine}\n'
              'Kernel: {s.release}\n'
              'CPU: {cpu_count}\n').format(s=uname, cpu_count=mp.cpu_count())
    osinfo += '\n'

    renames = {'opencv-python':'cv2', 'scikit-learn':'sklearn'}
    excludes = ['python-dateutil', 'threadpoolctl']
    dependencies = [ renames[i] if i in renames.keys() else i for i in dependencies ]
    dependencies = [ i for i in dependencies if not i in excludes ]
    deps = ('Dependencies\n'
            '------------\n')
    deps += '\n'.join( '{pkg.__name__}: {pkg.__version__}'.format(pkg=__import__(dep)) for dep in dependencies )

    print(header + general + osinfo + deps)
    return None
