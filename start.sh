#!/bin/bash
export PYTHONPATH=/efs/www/dime/coins/DimeCoins

/usr/local/bin/python /efs/www/dime/api/DimeAPI/manage.py runserver 172.31.2.86:10006
