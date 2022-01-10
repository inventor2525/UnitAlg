from setuptools import setup

setup(
    name='UnitAlg',
    version='0.1.0',
    author='Charlie Angela Mehlenbeck',
    author_email='charlie_inventor2003@yahoo.com',
    packages=['UnitAlg'],
    py_modules=[],
    scripts=[],
    url='https://github.com/inventor2525/UnitAlg',
    license='LICENSE.txt',
    description='A numpy based Linear Algebra framework inspired by Unity, for python.',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy'
    ],
    python_requires='~=3.7'
)
