# coding=UTF-8
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open


# Get the long description from the relevant file
try:
  with open("README.md", "r") as fh:
    long_description = fh.read()
except:
    long_description = ''

    

setup(
    name="pykidgui", # Replace with your own username
    version="1.0.7",
    author="Ronan Bastos",
    author_email="ronanbastos@hotmail.com",
    description="Simple gui de python para uso rapido e pratico",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronanbastos/pykidgui",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


