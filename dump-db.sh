#!/bin/bash

if [ "$#" -lt 1 ]; then
    printf "Must provide an environment i.e. dev, stg, prod\n"
    exit 1
fi

mysqldump -u inventory -p inventory > db-snapshots/$1-$(date +"%Y%m%d%H%M%S").sql

exit 0

#
# Reload Data
#
# zcat db-snapshots/<env>-<date>.sql.gz | ./manage.py dbshell
# or
# zcat db-snapshots/<env>-<date>.sql.gz | mysql -u inventory -p inventory
#
