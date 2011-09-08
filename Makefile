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
all: .pkg/.stamp-h

.PHONY: check
check: .pkg/.stamp-h
	mkdir -p build/report
	.pkg/bin/python -Wall tests/manage.py test \
	  --settings=tests.settings \
	  --with-xunit \
	  --xunit-file="build/report/xunit.xml" \
	  --with-xcoverage \
	  --xcoverage-file="build/report/coverage.xml" \
	  --cover-package=django_patterns \
	  --cover-erase \
	  --cover-tests \
	  --cover-inclusive \
	  django_patterns

.PHONY: shell
shell: .pkg/.stamp-h
	.pkg/bin/python tests/manage.py shell_plus \
	  --print-sql \
	  --ipython

.PHONY: mostlyclean
mostlyclean:

.PHONY: clean
clean: mostlyclean
	-rm -rf build
	-rm -rf .pkg

.PHONY: distclean
distclean: clean
	-rm -rf .cache

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

.PHONY: dist
dist:

# ===--------------------------------------------------------------------===
# ===--------------------------------------------------------------------===

.cache/virtualenv/virtualenv-1.6.4.tar.gz:
	mkdir -p .cache/virtualenv
	sh -c "cd .cache/virtualenv && curl -O http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.6.4.tar.gz"

.pkg/.stamp-h: conf/requirements.*.pip .cache/virtualenv/virtualenv-1.6.4.tar.gz
	${MAKE} clean
	tar \
	  -C .cache/virtualenv --gzip \
	  -xf .cache/virtualenv/virtualenv-1.6.4.tar.gz
	mkdir -p .cache/pypi
	python .cache/virtualenv/virtualenv-1.6.4/virtualenv.py \
	  --clear \
	  --no-site-packages \
	  --distribute \
	  --never-download \
	  --prompt="(django-patterns) " \
	  .pkg
	rm -rf .cache/virtualenv/virtualenv-1.6.4
	mkdir -p .cache/pypi
	for reqfile in conf/requirements.*.pip; do \
	  .pkg/bin/python .pkg/bin/pip install \
	    --download-cache="`pwd`"/.cache/pypi \
	    -r $$reqfile; \
	done
	touch .pkg/.stamp-h

# ===--------------------------------------------------------------------===
# End of File
# ===--------------------------------------------------------------------===
