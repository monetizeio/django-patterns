# === makefile ------------------------------------------------------------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
# 
# RokuSigma Inc. (the “Company”) Confidential
#
# NOTICE: All information contained herein is, and remains the property of the
# Company. The intellectual and technical concepts contained herein are
# proprietary to the Company and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from the
# Company. Access to the source code contained herein is hereby forbidden to
# anyone except current Company employees, managers or contractors who have
# executed Confidentiality and Non-disclosure agreements explicitly covering
# such access.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of the
# Company. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE,
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS
# WRITTEN CONSENT OF THE COMPANY IS STRICTLY PROHIBITED, AND IN VIOLATION OF
# APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF
# THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
# USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
# ===----------------------------------------------------------------------===

.PHONY: all
all: build/.stamp-h

.PHONY: check
check: build/.stamp-h
	./build/bin/python -Wall tests/manage.py test \
	  --settings=tests.settings \
	  --with-coverage \
	  --cover-package=django_patterns \
	  --with-xunit \
	  --xunit-file="tests/log/nosetests.xml" \
	  --with-xcoverage \
	  --xcoverage-file="tests/log/coverage.xml" \
	  django_patterns

.PHONY: shell
shell: build/.stamp-h
	./build/bin/python tests/manage.py shell_plus \
	  --print-sql \
	  --ipython

.PHONY: mostlyclean
mostlyclean:

.PHONY: clean
clean: mostlyclean
	-rm -rf build

.PHONY: distclean
distclean: clean
	-rm -rf cache/pypi/*

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

.PHONY: dist
dist:

# ===--------------------------------------------------------------------===
# ===--------------------------------------------------------------------===

build/.stamp-h: conf/requirements.pip
	${MAKE} clean
	mkdir -p cache/pypi
	./sandbox/build/bin/virtualenv \
	  --clear \
	  --no-site-packages \
	  --distribute \
	  --never-download \
	  --prompt="(django-patterns) " \
	  build
	./build/bin/python build/bin/pip install \
	  --download-cache="`pwd`"/cache/pypi \
	  -r conf/requirements.pip
	touch build/.stamp-h

# ===--------------------------------------------------------------------===
# End of File
# ===--------------------------------------------------------------------===
