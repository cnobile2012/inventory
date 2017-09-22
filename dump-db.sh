#!/bin/bash

if [ "$#" -lt 1 ]; then
    printf "Must provide an environment i.e. dev, stg, prod\n"
    exit 1
fi

SNAPSHOT_DIR='db-snapshots'

if [ ! -d $SNAPSHOT_DIR ]; then
    mkdir $SNAPSHOT_DIR
fi

pg_dump --username=inventory -c --compress=9 -h localhost inventory > \
        $SNAPSHOT_DIR/$1-$(date +"%Y%m%d%H%M-%s").sql.gz

exit 0

#
# Reload Data
#
# zcat db-snapshots/<env>-<date>.sql.gz | ./manage.py dbshell
#
