from setuptools import setup

setup(
    name='UnitAlg',
    version='0.0.5',
    author='Charlie Angela Mehlenbeck',
    author_email='charlie_inventor2003@yahoo.com',
    packages=['UnitAlg'],
    py_modules=[],
    scripts=[],
    url='https://github.com/inventor2525/UnitAlg',
    license='LICENSE.txt',
    description='An un-described package.',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
        'OCC'
    ],
    python_requires='~=3.7'
)