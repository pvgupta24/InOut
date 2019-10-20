# SpeakInOut

Project made for InOut 6.0, 19-20th October, 2019.

## Introduction

### Features

# Installation

### Setting up the Virtual Environment

```bash
python3 -m venv env
cd env
source bin/activate
pip install --upgrade setuptools
```

### How to run?

```bash
git clone https://github.com/pvgupta24/InOut/
cd InOut/
pip install -r requirements.txt
cd speakInOut
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```