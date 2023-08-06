from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wheelsbyhasan',
    version='0.0.9',
    packages=setuptools.find_packages(),
    author='Hasan Abu-Rayyan',
    author_email='hasanaburayyan21@gmail.com',
    description='Cool First Wheel',
    python_requires='>=3.6'
)