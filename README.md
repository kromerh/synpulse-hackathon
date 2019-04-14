# synpulse-hackathon

# Instructions

- import json content into Alexa Developer console
- import lambda function into AWS lambda console, using Python3.7
- see the detailed documentation `Documentation synpulse hackathon.pdf` for instructions on how to use the Alexa skill

# Alexa Skill Json file

`heiko.Alexa_skill.json`

# lamda AWS function

- requires Python3.7

`lambda.py`


## Get AWS python package remote installed

- put in requirements.txt the packages

`pip install -r requirements.txt -t skill_env`

- copy the contents of the lambda/py folder into the skill_env folder.

- Pandas. Navigate to https://pypi.org/project/pandas/#files. Search for and download newest *manylinux1_x86_64.whl package. In my case for Python 3.6 is pandas-0.24.1-cp36-cp36m-manylinux1_x86_64.whl file.

- NumPy. Do the same for NumPy. File is numpy-1.16.1-cp36-cp36m-manylinux1_x86_64.whl.

- 
