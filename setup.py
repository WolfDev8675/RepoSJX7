#!usr/bin/python
""" Setup for package """
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2",'Analysis.py','DataAccess.py','Intelligence.py','Visuals.py']

setup(
    name="CaseStudy_Backend",
    version="0.0.1",
    author="Bishal Biswas - github.com/WolfDev8675",
    author_email="b.biswas_94587@ieee.org",
    description="Support package for checking Brent Oil price fluctuation determination",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/WolfDev8675/RepoSJX7/tree/CaseStudy_backend",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)