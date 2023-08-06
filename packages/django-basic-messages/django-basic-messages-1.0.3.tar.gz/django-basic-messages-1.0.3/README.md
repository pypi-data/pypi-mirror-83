# django_messages

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3523210.svg)](https://doi.org/10.5281/zenodo.3523210)

<!-- TOC -->

A simple re-usable Django application for storing messages from within django that should support both Python 2 and 3.  It only uses admin and ORM, no external-facing templates or pages.

To start, just puts them in a database.  Eventually, might add ways to send them other places as well (email, message queue, etc.).

# Installation

Assumptions:

- You already have a django project, and your database is configured and tested.  If you don't, see the django tutorial for instructions on creating a django project.
- You are using a virtualenv, such that you don't have to run `pip` as root.  If not, add `sudo` in front of `pip` commands, or open a shell as root.

## Dependencies

- install python_utilites in your django project:

        pip install python-utilities-jsm
        
- install django_config and its requirements in your django project:

        pip install django-basic-config
        
- install this project.  Either:

    - install using pip:

            pip install django-basic-messages

    - or install from source:

            cd <django_project_directory>
            git clone https://github.com/jonathanmorgan/django_messages.git
            pip install -r ./django_messages/requirements.txt

# Configuration

Update `settings.py` so that `taggit`, `django_config` and `django_messages` are in your `INSTALLED_APPS`.  Use the new-style apps.py syntax for `django_config` - `'django_config.apps.Django_ConfigConfig'`, and `django_messages` - `'django_messages.apps.DjangoMessagesConfig'`.  The result should look like:

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
        'taggit',
        'django_config.apps.Django_ConfigConfig',
        'django_messages.apps.DjangoMessagesConfig',
    ]

# Usage

To create and retrieve messages:

    # django_messages imports
    from django_messages.models import Message

    # set up message values
    application = "unit_test"
    message = "test message"
    message_type = "test message type"
    label = "test"
    status = Message.STATUS_NEW
    tag_list = [ "awesome", "test" ]
    
    # create instance
    # make instance
    message_instance = Message.create_message( message,
                                               message_type_IN = message_type,
                                               application_IN = application,
                                               label_IN = label,
                                               tag_list_IN = tag_list,
                                               status_IN = status )

    # get all messages
    message_qs = Message.objects.all()
    
    # get message for application
    message_qs = message_qs.filter( application = application )
    message_instance = message_qs.get()

# Database

In your django project folder, run the `migrate` command to create database table(s) for newly installed application(s):

    python manage.py migrate

# Testing

The sourcenet project has a small but growing set of unit tests that once can auto-run. These tests use django's testing framework, built on top of the Python `unittest` package.

## Unit tests

### Configuration

#### Database configuration

In order to run unit tests, your database configuration in `settings.py` will need to be connecting to the database with a user who is allowed to create databases. When django runs unit tests, it creates a test database, then deletes it once testing is done.

- _NOTE: This means the database user you use for unit testing SHOULD NOT be the user you'd use in production. The production database user should not be able to do anything outside a given database._

### Running unit tests

In your django project folder, run the `test` command to run unit tests for this project:

    python manage.py test django_messages.tests

# License

Copyright 2020 Jonathan Morgan

This file is part of [https://github.com/jonathanmorgan/django_messages](https://github.com/jonathanmorgan/django_messages).

django_messages is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

django_messages is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with [https://github.com/jonathanmorgan/django_messages](https://github.com/jonathanmorgan/django_messages).  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
