# Odoo Attendances

## Simple Selenium script to fill attendances for employeer in ODOO

### Author: Andrzej Michalski, Cervi Robotics

### All rights reserved (c)

Script fills attendances in ODOO from the last record to today.
User have to specify: login, password, check in and check out in file "login.txt".

Script requires:
Python 3 (3.6 in this case), GIT, VirtualEnv, Chrome Web Browser

Moreover chromedriver for selenium on disk (https://selenium-python.readthedocs.io/installation.html)

Instalation Linux (Ubuntu):
In command line type
1. git clone https://github.com/andmichalski/odoo_attendances
2. cd odoo_attendances/
3. Download and unpack chromedriver to folder "odoo_attendances" from website http://chromedriver.chromium.org/downloads
4. (in folder odoo_attendances type) virtualenv --python=python3 venv
5. . ./venv/bin/activate
6. pip install -r requirements.txt
7. Edit file "login.txt" - specify Login, password, check in and check out
8. python3 odoo_attendances.py
