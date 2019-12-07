**********************************
Installation of Basic Requirements
**********************************

On Ubuntu Basic Packages Need to be Installed
=============================================

.. code-block:: console

    $ sudo apt ubuntu-dev-tools python-setuptools python3-dev OR python-dev
               postgresql postgresql-client postgresql-contrib
               postgresql-server-dev-all redis-server redis-tools libssl-dev

Python Packages Need to be Installed
====================================

.. code-block:: console

    $ sudo easy_install3 pip
    # Newer systems no longer have ``easy_install`` for Python 3
    # installed, however I have found the commands below to work.
    $ sudo python3 /usr/lib/python3/dist-packages/easy_install.py pip
    $ sudo -H pip3 install virtualenvwrapper

Virtual Wrapper Initialization
==============================

Use your favorite editor to add the following lines at the end of your
``.bashrc`` file.

.. code-block:: bash

    # Setup the Python virtual environment.
    VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source /usr/local/bin/virtualenvwrapper.sh

Create the Virtual Environment
==============================

.. code-block:: console

    $ mkvirtualenv inventory

Install the Inventory Requirements
==================================

.. code-block:: console

    $ pip install -r requirements/<env file>.txt
