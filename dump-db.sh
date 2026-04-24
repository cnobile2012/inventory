#!/bin/bash

if [ "$#" -lt 1 ]; then
    printf "Must provide an environment i.e. dev, stg, prod\n"
    exit 1
fi

DIR="db-snapshots"

if [ ! -d {DIR} ]; then
    mkdir ${DIR}

FILE=$1-$(date +"%Y%m%d%H%M%S").sql

mysqldump -u inventory -p inventory > ${DIR}/${FILE}
gzip -9 ${DIR}/${FILE}

exit 0

#
# Reload Data
#
# zcat db-snapshots/<env>-<date>.sql.gz | ./manage.py dbshell
# or
# zcat db-snapshots/<env>-<date>.sql.gz | mysql -u inventory -p inventory
#
