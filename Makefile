#
# Development by Carl J. Nobile
#
# $Author: cnobile $
# $Date: 2010-10-05 12:28:39 -0400 (Tue, 05 Oct 2010) $
# $Revision: 26 $
#

PREFIX		= $(shell pwd)
PACKAGE_DIR	= $(shell echo $${PWD\#\#*/})
APACHE_DIR	= $(PREFIX)/apache
DOCS_DIR	= $(PREFIX)/docs
LOGS_DIR	= $(PREFIX)/logs
PIP_ARGS	=

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          $(PACKAGE_DIR))

.PHONY	: coverage
coverage: clean
	@rm -rf $(DOCS_DIR)/htmlcov
	coverage erase
	coverage run ./manage.py test
	coverage report
	coverage html

.PHONY	: sphinx
sphinx  : clean
	(cd $(DOCS_DIR); make html)

.PHONY	: install-dev
install-dev:
	pip install $(PIP_ARGS) -r requirements/development.txt

.PHONY	: install-prd
install-prd:
	pip install $(PIP_ARGS) -r requirements/development.txt

.PHONY	: install-stg
install-stg:
	pip install $(PIP_ARGS) -r requirements/stage.txt

#----------------------------------------------------------------------
clean	:
	cleanDirs.sh clean
	@(cd ${DOCS_DIR}; make clean)

clobber	: clean
	@(cd $(DOCS_DIR); make clobber)
	@rm -f $(LOGS_DIR)/*.log*
