from distutils.core import setup

from setuptools import find_packages

setup(
    name='strict-hint',
    packages=find_packages(exclude=['tests']),
    version='0.1.0',
    description='Strict type runtime checks for arguments and return types.',
    author='Michal Wachowski',
    author_email='wachowski.michal@gmail.com',
    url='https://github.com/potfur/strict-hint',
    download_url='https://github.com/potfur/strict-hint/tarball/0.1',
    keywords=['type hint', 'type validation', 'type declaration',
              'argument type', 'return type'],
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
