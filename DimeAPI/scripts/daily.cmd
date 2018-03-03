
set WORKING_DIR=C:\Users\kevin\OneDrive\Work\software\dime\DimeAPI
set PYTHONPATH=C:\Users\kevin\OneDrive\Work\software\dime\DimeCoins
set DJANGO_SERVER_TYPE=dev
set DJANGO_SETTINGS_MODULE=DimeAPI.settings.dev
cd %WORKING_DIR%
%PYTHON% manage.py GenerateDimeHistory
%PYTHON% manage.py CalculateDime
