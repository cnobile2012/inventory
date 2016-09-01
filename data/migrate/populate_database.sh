#!/bin/bash
###############################
#
# Populate all database tables.
#
###############################

PWD=$(pwd)

cd $PWD

# Creates a project record and imports all the category records.
./migrate_categories.py -p
# Creates a project if not already done then imports all the supplier records.
./migrate_suppliers.py -p
# Creates a project if not already done then creates a location default record
# and imports all the location format and location code records.
./migrate_location.py -p
# Imports all the item and cost records then creates all the dynamic_column,
# column collection, and key value records.
./migrate_items.py -p
