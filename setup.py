import pyaehw4a1
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyaehw4a1',
    version=pyaehw4a1.__version__,
    description='Python interface for Hisense AEH-W4A1 module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bannhead/pyaeh-w4a1',
    author='Davide Varricchio',
    author_email='davide.varricchio@gmail.com',
    license='Apache 2.0',
    packages=['pyaehw4a1'])

