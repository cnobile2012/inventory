**********************************
Installation of Basic Requirements
**********************************

On Ubuntu Basic Packages Need to be Installed
=============================================

Use ``sudo apt-get install`` or ``sudo aptitude install``.


ubuntu-dev-tools python-setuptools python3-dev OR python-dev
postgresql postgresql-client postgresql-contrib postgresql-server-dev-all
redis-server redis-tools libssl-dev

Python Packages Need to be Installed
====================================

``$ sudo easy_install pip``

``$ sudo pip install virtualenvwrapper``

Virtual Wrapper Initialization
==============================

Use your favorite editor to add the following lines at the end of your
``.bashrc`` file.

``# Setup the Python virtual environment.``
``. /usr/local/bin/virtualenvwrapper.sh``

Create the Virtual Environment
==============================

``$ mkvirtualenv inventory``

Install the Inventory Requirements
==================================

``$ pip install -r requirements/<env file>.txt``
