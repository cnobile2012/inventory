# Installation of Basic Requirements

## On Ubuntu Basic Packages Need to be Installed

Use `sudo apt-get install` or `sudo aptitude install`.

ubuntu-dev-tools python-setuptools

mariadb-client mariadb-server libmariadbclient-dev libmariadbd-dev

redis-server redis-tools

libssl-dev

## Python Packages Need to be Installed

$ `sudo easy_install pip`

$ `sudo pip install virtualenvwrapper`

## Create the Virtual Environment

$ `mkvirtualenv inventory`

## Install the Inventory Requirements

$ `pip install -r requirements/<env file>.txt`
