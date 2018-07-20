from setuptools import setup
import os
import pyaimms

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='pyaimms',
        version=pyaimms.__version__,
        packages=['pyaimms'],
        url='',
        license='',
        author='wsun',
        author_email='w.sun@ed.ac.uk',
        description='python handler for AIMMS',
        long_description=read('README.rst'),
        install_requires=['pandas',
                          'win32com']
        )
