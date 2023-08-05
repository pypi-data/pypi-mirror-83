import setuptools
import sys

if 'sdist' not in sys.argv:
    raise Exception("oh shit waddup! \n you probably wanted to install factoryboy")

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="factoryboi",
    version="0.0.2",
    author="Hubert Bryłkowski",
    author_email="hubert@brylkowski.com",
    description="package that will tell you have a typo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

