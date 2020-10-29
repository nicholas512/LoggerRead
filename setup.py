from setuptools import setup


setup(
    name='Pyrmafrost',
    version=__version__,
    description='A simple module for reading Onset HOBO data logger data',
    long_description=open('README.md').read(),
    #url='https://github.com/nicholas512/Pyrmafrost',
    author='Nick Brown',
    author_email='',
    py_modules=['libraries'],
    #test_suite='test_readers',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
)
