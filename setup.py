from setuptools import setup

__version__ = "0.0.1"

setup(
    name='LoggerReader',
    version=__version__,
    description='A simple module for reading various datalogger output files',
    long_description=open('README.md').read(),
    #url='https://github.com/nicholas512/Pyrmafrost',
    author='Nick Brown',
    author_email='',
    py_modules=['LoggerReader'],
    install_requires=['pandas']
    #test_suite='test_readers',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
)
