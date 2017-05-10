from distutils.core import setup

from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='strict-hint',
    packages=find_packages(exclude=['tests']),
    version='0.2.4',
    description='Strict type runtime checks for arguments and return types.',
    long_description=readme,
    author='Michal Wachowski',
    author_email='wachowski.michal@gmail.com',
    url='https://github.com/potfur/strict-hint',
    download_url='https://github.com/potfur/strict-hint/archive/0.2.4.tar.gz',
    keywords=[
        'type hint',
        'type validation',
        'type declaration',
        'argument type',
        'return type'
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-flake8',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
