from setuptools import find_packages, setup

setup(
    name='csvHandler',
    packages=find_packages(),
    version='0.0.3',
    description='csv in memory paginator',
    author='mahmoud',
    license='MIT',
    install_requires=['pandas']
)