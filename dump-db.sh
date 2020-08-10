#!/bin/bash
#
# Usage: -u -- DB user (default is "inventory")
#        -h -- host (default is localhost)
#        -e -- Prefixed environment tag (ex. dev, stg, prod, but can be longer)
#        -D -- Database name (defaults to "inventory")
#        -d -- Directory to put dump files (default is "db-snapshots").
#
# You will be prompted for the DB user's password.
#
# Reload data
#
# zcat db-snapshots/<env>-<date>.sql.gz | ./manage.py dbshell
#

set -e
set -u
set -o pipefail

USER="inventory"
HOST="localhost"
ENV=""
DB="inventory"
DIR="db-snapshots"

while getopts 'u:h:e:D:d:' opt; do
    case ${opt} in
        u )
            USER="$OPTARG"
            ;;
        h )
            HOST="$OPTARG"
            ;;
        e )
            ENV="$OPTARG"
            ;;
        D )
            DB="$OPTARG"
            ;;
        d )
            DIR="$OPTARG"
            ;;
        \? )
            printf "Usage: $(basename $0) [-u <db user>] [-h <hostname>] [-e <environment tag>] [-d <directory>]\n"
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))
printf "Options--user: %s, host: %s, env: %s, dir: %s\n" "$USER" "$HOST" \
       "$ENV" "$DIR"

if [ "$ENV" == "" ]; then
    printf "Must provide an environment i.e. dev, stg, prod\n"
    exit 1
fi

if [ ! -d "$DIR" ]; then
    mkdir "$DIR"
fi

pg_dump --username="$USER" -c --compress=9 -h "$HOST" "$DB" > \
        "$DIR"/"$ENV"-$(date +"%Y%m%d%H%M-%s").sql.gz

exit 0
