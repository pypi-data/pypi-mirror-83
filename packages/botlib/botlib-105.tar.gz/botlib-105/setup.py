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
    version='105',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="the bot library",
    long_description=read(),
    license='Public Domain',
    install_requires=["olib"],
    packages=["bot", "botmod"],
    namespace_packages=["bot", "botmod"],
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
