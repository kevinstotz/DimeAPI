#!/bin/bash

export PYTHONPATH=/opt/www/dime/api/DimeAPI

/usr/local/bin/python /opt/www/dime/api/DimeAPI/manage.py runserver 172.31.2.86:10006

