#!/bin/bash
#
# Create a starter DB with basic data. This DB can be used as a starting point
# for migrating data.
#

printf "Create the DB schema\n"
sudo -u postgres psql template1 -f db/create_schema.ddl

printf "\nInstall the DB schema\n"
./manage.py migrate

printf "\nCreate a Django superuser:\n"
./manage.py createsuperuser

printf "\nPopulate the DB with regions data:\n"
./manage.py populate_regions -a @data/regions/populate-regions.conf

printf "Create the backup:\n"
./dump-db.sh -e dev-before-data-migration

exit 0
