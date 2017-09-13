python_version := 3.6
src_dir := src
lintable := $(src_dir) test

.PHONY: check
check: pylint pep8 test

.PHONY: test
test: ve
	. ve/bin/activate && find test/unit -name test*.py | PYTHONPATH=. xargs -n 1 python3

.PHONY: clean
clean:
	rm -rf ve/

ve:
	virtualenv $@ --python=python$(python_version)
	. ./$@/bin/activate && pip$(python_version) install -r requirements.txt

.PHONY: repl
repl:
	. ve/bin/activate && python

.PHONY: pylint
pylint: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs \
	pylint --rcfile ./.pylintrc -d missing-docstring -d line-too-long -d invalid-name -d redefined-outer-name

.PHONY: pep8
pep8: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pep8 --max-line-length=110

.PHONY: run
run: ve
	@. ve/bin/activate && python3 $(src_dir)/engine.py
