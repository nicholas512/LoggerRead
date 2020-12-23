from setuptools import setup

__version__ = "0.0.2"

setup(
    name='LoggerReader',
    version=__version__,
    description='A simple module for reading various datalogger output files',
    long_description=open('README.md').read(),
    # url='https://github.com/nicholas512/Pyrmafrost',
    author='Nick Brown',
    author_email='',
    python_requires='>3.5.2',
    py_modules=['LoggerReader'],
    install_requires=['pandas'],
    # test_suite='test_readers',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    include_package_data=True,
    package_data={'LoggerReader': ['sample_files/*']}
)
