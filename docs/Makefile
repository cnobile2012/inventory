#
# Makefile
# Development by Carl J. Nobile
#
# $Author: cnobile $
# $Date: 2009-08-29 02:33:36 $
# $Revision: 1.1.1.1 $
#

FQDN		= $(shell hostname --fqdn)
DOC_DIR		= $(shell pwd)
API_DIR		= api
URL		= http://${FQDN}${DOC_DIR}/${API_DIR}/index.html
TARBALL_NAME	= inventory

all	: api-docs

#----------------------------------------------------------------------
api-docs:
	@(cd ..; epydoc -v --docformat epytext \
          --name "TetraSys Inventory" -o docs/api --show-private \
          --show-imports --graph all --url "${URL}" \
          apache/*.wsgi inventory/*.py inventory/apps/items/*.py \
          inventory/apps/login/*.py inventory/apps/reports/*.py \
          inventory/apps/maintenance/*.py inventory/apps/regions/*.py \
          inventory/apps/utils/*.py \
         )
#----------------------------------------------------------------------
tar	:
	@(ln -s ${API_DIR} ${TARBALL_NAME}; \
          tar -chzvf ${TARBALL_NAME}.tar.gz ${TARBALL_NAME})
#----------------------------------------------------------------------

clean	:
	@rm -f *~ \#* .\#*

clobber	: clean
	@rm -rf ${API_DIR} ${TARBALL_NAME} ${TARBALL_NAME}.tar.gz 
