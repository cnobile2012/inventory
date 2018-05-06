#!/bin/bash
#
# Run a single test file with coverage.
#

PREFIX=$(pwd)
COVERAGE_FILE=.coveragerc
COVERAGE_DIR=${PREFIX}/.coverage_tests

coverage erase --rcfile=${COVERAGE_FILE}
rm -rf ${COVERAGE_DIR}
mkdir -p ${COVERAGE_DIR}
coverage run manage.py test $1 $2
mv .coverage.* ${COVERAGE_DIR}
coverage combine --rcfile=${COVERAGE_FILE} ${COVERAGE_DIR}
coverage report -m --rcfile=${COVERAGE_FILE}
