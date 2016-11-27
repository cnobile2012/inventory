/*
 * $ sudo -u postgres psql template1 -f db/create_schema.ddl
 */

DROP DATABASE IF EXISTS inventory;
CREATE DATABASE inventory;

BEGIN;
CREATE USER inventory WITH PASSWORD 'inventory';
ALTER USER inventory CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE inventory TO inventory;
ALTER ROLE inventory SET client_encoding TO 'utf8';
ALTER ROLE inventory SET default_transaction_isolation TO 'read committed';
ALTER ROLE inventory SET timezone TO 'UTC';
COMMIT;
