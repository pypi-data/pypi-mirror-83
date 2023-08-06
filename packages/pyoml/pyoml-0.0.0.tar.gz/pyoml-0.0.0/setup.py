import setuptools


DISTNAME = 'pyoml'
DESCRIPTION = 'Online Machine Learning algorithms written in python'
MAINTAINER = 'Murilo Camargos'
MAINTAINER_EMAIL = 'murilo.camargosf@gmail.com'
URL = 'https://github.com/murilocamargos/pyoml'
LICENSE = 'MIT'
VERSION = '0.0.0'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(name=DISTNAME,
                 maintainer=MAINTAINER,
                 maintainer_email=MAINTAINER_EMAIL,
                 description=DESCRIPTION,
                 license=LICENSE,
                 version=VERSION,
                 long_description=LONG_DESCRIPTION,
                 long_description_content_type="text/markdown",
                 url=URL,
                 packages=setuptools.find_packages(),
                 classifiers=['Intended Audience :: Science/Research',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved',
                              'Programming Language :: C',
                              'Programming Language :: Python',
                              'Topic :: Software Development',
                              'Topic :: Scientific/Engineering',
                              'Operating System :: Microsoft :: Windows',
                              'Operating System :: POSIX',
                              'Operating System :: Unix',
                              'Operating System :: MacOS',
                              'Programming Language :: Python :: 3',
                              'Programming Language :: Python :: 3.5',
                              'Programming Language :: Python :: 3.6',
                              'Programming Language :: Python :: 3.7',
                              ('Programming Language :: Python :: '
                              'Implementation :: CPython'),
                              ('Programming Language :: Python :: '
                              'Implementation :: PyPy')
                              ],
                 python_requires=">=3.5")
