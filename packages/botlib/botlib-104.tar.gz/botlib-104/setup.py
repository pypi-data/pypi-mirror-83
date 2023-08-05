# setup.py
#
#

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='104',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="""framework to program bots""",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    namespace_packages=["bot"],
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
