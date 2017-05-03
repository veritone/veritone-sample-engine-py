python_version := 3.6
src_dir := src

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

repl:
	. ve/bin/activate && python

lintable := $(src_dir) test

.PHONY: pylint
pylint: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pylint --rcfile ./.pylintrc -d missing-docstring

.PHONY: pep8
pep8: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pep8 --max-line-length=100

ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: run
run: ve
	@. ve/bin/activate && python3 $(src_dir)/engine.py $(RUN_ARGS)
