from setuptools import find_packages, setup
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))

def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
    name="LibcSearcher",
    version="1.1.5",
    description="Python wrapper for libc-database.",
    author="IZAY01",
    author_email="IZAYOInt0x80@gmail.com",
    platforms=["any"],
    license="BSD",
    url="https://github.com/IZAY01/LibcSearcher",
    long_description=read_file('README.md'), 
    long_description_content_type="text/markdown",
    install_requires=[
        'requests',
    ],
    packages=find_packages(), )
