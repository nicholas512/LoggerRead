from setuptools import setup

__version__ = "0.1.0"

setup(
    name='LoggerRead',
    version=__version__,
    description='A simple module for reading various datalogger output files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nicholas512/LoggerRead',
    author='Nick Brown',
    python_requires='>3.6',
    py_modules=['LoggerReader'],
    install_requires=['pandas'],
    # test_suite='test_readers',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta'          
    ],
    include_package_data=True,
    package_data={'LoggerReader': ['sample_files/*']}
)
