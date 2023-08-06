from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.rst")) as f:
    long_description = f.read()

requirements = ["requests", "PyJWT"]

setup(
    name="mercuryclient",
    version="0.5.0",
    description="Python SDK for Mercury service",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://bitbucket.org/esthenos/mercury",
    author="Esthenos Technologies Private Limited",
    author_email="dinu@esthenos.com",
    license="Proprietary License",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={"dev": ["pre-commit", "wheel", "twine"]},
    zip_safe=False,
)
