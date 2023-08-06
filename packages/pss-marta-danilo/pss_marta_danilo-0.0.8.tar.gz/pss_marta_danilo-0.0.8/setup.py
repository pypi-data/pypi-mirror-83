import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pss_marta_danilo",
    version = "0.0.8",
    author = "Danilo Marta",
    description = ("..."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/pss_marta_danilo",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
