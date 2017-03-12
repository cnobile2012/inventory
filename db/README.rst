**************
Setup Database
**************

Log into postgres::

  $ sudo -u postgres psql template1

Run the next two commands::

  DROP DATABASE IF EXISTS inventory;

  CREATE DATABASE inventory;

If the user role does not exist run the next two lines::

  CREATE USER inventory WITH PASSWORD 'inventory';

  ALTER USER inventory CREATEDB;

These commands are always run::

  GRANT ALL PRIVILEGES ON DATABASE inventory TO inventory;

  ALTER ROLE inventory SET client_encoding TO 'utf8';

  ALTER ROLE inventory SET default_transaction_isolation TO 'read committed';

  ALTER ROLE inventory SET timezone TO 'UTC';

Run migrations::

  $ ./manage.py makemigrations accounts categories invoices locations projects regions suppliers

  $ ./manage.py migrate

Create user account::

  $ ./manage.py createsuperuser

Populate the regions::

  $ ./manage.py populate_regions -a @data/regions/populate-regions.conf

Populate old data::

  $ (cd data/migrate; ./populate_database.sh)
