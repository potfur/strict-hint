from distutils.core import setup

from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

ver = '0.3.0'
setup(
    name='strict-hint',
    packages=find_packages(exclude=['tests']),
    version=ver,
    description='Strict type runtime checks for arguments and return types.',
    long_description=readme,
    author='Michal Wachowski',
    author_email='wachowski.michal@gmail.com',
    url='https://github.com/potfur/strict-hint',
    download_url='https://github.com/potfur/strict-hint/archive/%s.tar.gz' % ver,
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
        'flake8',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
