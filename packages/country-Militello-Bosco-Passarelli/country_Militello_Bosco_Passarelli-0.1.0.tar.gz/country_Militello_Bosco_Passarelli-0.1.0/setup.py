import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="country_Militello_Bosco_Passarelli", 
    version="0.1.0",
    author="Patrick Militello, Alessandro Bosco, Raffaello Passarelli",
    author_email="p.militello@campus.unimib.it, a.bosco10@campus.unimib.it, r.passarelli@campus.unimib.it",
    description="Applicativo per semplici calcoli sulla popolazione di 10 paesi del mondo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/theunusual/2020_assignment1_countries",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)

