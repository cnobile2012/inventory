#
# Development by Carl J. Nobile
#
# $Author: cnobile $
# $Date: 2010-10-05 12:28:39 -0400 (Tue, 05 Oct 2010) $
# $Revision: 26 $
#

PREFIX		= $(shell pwd)
BASE_DIR	= $(shell basename $(PREFIX))
PACKAGE_DIR	= $(BASE_DIR)
APACHE_DIR	= $(PREFIX)/apache
DOCS_DIR	= $(PREFIX)/docs
LOGS_DIR	= $(PREFIX)/logs
RM_REGEX	= '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;

#----------------------------------------------------------------------
all	: tar

.PHONY	: tar
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz $(PACKAGE_DIR))

.PHONY	: coverage
coverage: clean
	@rm -rf $(DOCS_DIR)/htmlcov
	coverage erase
	coverage run ./manage.py test
	coverage report
	coverage html

.PHONY	: flake8
flake8	:
#       Error on syntax errors or undefined names.
	flake8 . --select=E9,F7,F63,F82 --show-source
#       Warn on everything else.
	flake8 . --exit-zero

#----------------------------------------------------------------------
.PHONE	: clean
clean	:
	$(shell $(RM_CMD))

.PHONE	: clobber
clobber	: clean
	@(cd $(DOCS_DIR); make clobber)
	@rm -f $(LOGS_DIR)/*.log*
