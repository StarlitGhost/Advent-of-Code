from setuptools import find_packages, setup

setup(
    name='GhostyUtils',
    packages=find_packages(exclude=['tests']),
    version='0.1.0',
    description='A library of commonly needed functions and algorithms for Advent of Code puzzles',
    author='StarlitGhost',
    author_email='ghosty@starlitghost.xyz',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.3'],
    test_suite='tests',
)
