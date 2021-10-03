#!usr/bin/python

from setuptools import setup

setup(
   name='CaseStudy_Backend',
   version='0.1',
   description='Case Study for Predicting Brent Oil Price fluctuations. Work done for Post Graduate Diploma in Data Science from BSE in collaboration with MAKAUT',
   author='[Bishal Biswas(@WolfDev8675)](https://github.com/WolfDev8675)',
   author_email='b.biswas_94587@ieee.org',
   packages=['CaseStudy_Backend'],  #same as name
   install_requires=['pandas','numpy','matplotlib','statsmodel','sklearn'], #external packages as dependencies
)