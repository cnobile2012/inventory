/*
 * $ sudo su - postgres psql template1
 * \i path/to/inventory/db/create_schema.ddl
 */

BEGIN;
DROP DATABASE IF EXISTS inventory;
CREATE DATABASE inventory;

//CREATE USER inventory WITH PASSWORD 'inventory';
//ALTER USER inventory CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE inventory TO inventory;
ALTER ROLE inventory SET client_encoding TO 'utf8';
ALTER ROLE inventory SET default_transaction_isolation TO 'read committed';
ALTER ROLE inventory SET timezone TO 'UTC';
COMMIT;
