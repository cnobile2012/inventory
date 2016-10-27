#!/bin/bash
#
# Run a single test file with coverage.
#
coverage erase
coverage run manage.py test $1
coverage report
