# APP_MODULE is APP_NAME unless set elsewhere
APP_MODULE          ?= $(shell echo $(APP_NAME)| tr - _ )
SRC_DIR             ?= .
VERSION_FILE        ?= $(SRC_DIR)/$(APP_MODULE)/__init__.py
BACKUP_EXT          ?= dist-backup
LOCAL_PACKAGES_DIR  ?= ../generated/local-packages
PYTHON_VERSION_RAW  ?=
TWINE_UPLOAD_TARGET ?= dist/*
TWINE_GUARD         := $(shell command -v twine 2> /dev/null)
IT_TESTS_TARGET     ?= .
TOX_ARGS            ?=

.PHONY: check-twine
check-twine: ## Check if twine is installed 🙉
	@echo "+ $@"
ifndef TWINE_GUARD
	$(error "twine is not available please install it with 'pip install twine'")
endif
	@echo "Found twine (and that's a good news)"


.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	@echo "+ $@"

.PHONY: clean-build
clean-build: check-find ## Remove build artifacts
	@echo "+ $@"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(FIND_CMD) . -name '*.egg-info' -exec rm -fr {} +
	$(FIND_CMD) . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: check-find ## Remove Python file artifacts
	@echo "+ $@"
	$(FIND_CMD) . -name '*.pyc' -exec rm -f {} +
	$(FIND_CMD) . -name '*.pyo' -exec rm -f {} +
	$(FIND_CMD) . -name '*~' -exec rm -f {} +
	$(FIND_CMD) . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts
	@echo "+ $@"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: style
style: SHELL := $(WHICH_BASH)
style: check-venv-is-ready ## ▶ force style with black and isort
	@echo "+ $@"
	@echo "Enforce code format with black"
	@black --line-length 119 .
	@echo "Ordering import with isort..."
	@isort --line-width 119 --dt --profile black .
	@echo "🦾 Done!"

.PHONY: lint
lint: SHELL := $(WHICH_BASH)
lint: check-venv-is-ready # ▶ Run tox -e linters
	@echo "+ $@"
	@declare -a tox_args=(); \
	if [ -n "$(TOX_ARGS)" ]; then \
		tox_args+=($(TOX_ARGS)); \
	fi; \
	tox $${tox_args[@]} -e linters

.PHONY: tests
tests: SHELL := $(WHICH_BASH)
tests: check-venv-is-ready ## ▶ Run tests quickly with the default Python
	@echo "+ $@"
	@declare -a tox_args=(); \
	if [ -n "$(TOX_ARGS)" ]; then \
		tox_args+=($(TOX_ARGS)); \
	fi; \
	tox $${tox_args[@]} -e py3

.PHONY: test
test: tests ## Wrapper, same as the 'tests' target
	@echo "+ $@"

.PHONY: unit-tests
unit-tests: tests ## Wrapper, same as the 'tests' target
	@echo "+ $@"

.PHONY: integration-tests
integration-tests: check-venv-is-ready ## ▶ Run integration tests (if any)
	@echo "+ $@"
	cd $(IT_TESTS_TARGET); bats .

.PHONY: integration-test
integration-test: integration-tests ## Wrapper, same as the 'integration-tests' target

.PHONY: dist
dist: SHELL := $(WHICH_BASH)
dist: check-venv-is-ready ## ▶ Build python3 package
	@echo "+ $@"
	@echo "backuping version file [$(VERSION_FILE)]"
	cp $(VERSION_FILE) $(VERSION_FILE).$(BACKUP_EXT)
	@echo "setting version from git"
	# Let's provide a PEP 440 compatible version https://www.python.org/dev/peps/pep-0440/
	@if [[ "$(GIT_REF_SAFE_NAME)" == v* ]]; then \
		if [ -z "$(PYTHON_VERSION_RAW)" ]; then \
			PYTHON_VERSION_RAW=$$(echo $(GIT_REF_SAFE_NAME) | tr -d "v"); \
		fi; \
		PYTHON_VERSION=$${PYTHON_VERSION_RAW}+$(GIT_SHA1) ;\
	else \
		if [ -z "$(PYTHON_VERSION_RAW)" ]; then \
			PYTHON_VERSION_RAW=0.0.0; \
		fi; \
		PYTHON_VERSION=$${PYTHON_VERSION_RAW}+git.$(GIT_SHA1_DIRTY_MAYBE_DOT) ;\
	fi; \
	echo "Computed PYTHON_VERSION as [$${PYTHON_VERSION}]"; \
	sed "s/0\.0\.0+dev\.version/$${PYTHON_VERSION}/" $(VERSION_FILE) > .tmp
	@mv .tmp $(VERSION_FILE)
	@if [ -f pyproject.toml ]; then \
		echo "Found a [pyproject.toml] file, running 'build'"; \
		python -m build; \
	else \
		echo "No [pyproject.toml] file, running legacy package build command"; \
		python setup.py sdist; \
	fi

	@echo "restoring version file"
	@mv $(VERSION_FILE).$(BACKUP_EXT) $(VERSION_FILE)

.PHONY: package
package: dist

.PHONY: build
build: lint tests ## ▶ lint and test all in one

.PHONY: dist-upload
dist-upload: check-venv-is-ready check-twine ## Upload the python3 package to pypi
	twine upload --repository-url $(GAR_PYTHON_URL)/ $(TWINE_UPLOAD_TARGET)

.PHONY: local-package
local-package: check-pwd clean dist ## Store artifact in the local-package storage
	@echo "+ $@"
	@mkdir -p $(LOCAL_PACKAGES_DIR)
	@cp dist/$(APP_NAME)-*.tar.gz $(LOCAL_PACKAGES_DIR)/$(APP_NAME).tar.gz

.PHONY: check-pwd
check-pwd: ## Check that we are in a python sub directory
	@echo "+ $@"
	@subdir=$$(echo $(PWD) | rev | cut -d "/" -f 2 | rev); \
	if [[ "$$subdir" != "python" ]]; then \
		echo "You don't seem to be in a 'python' sub directory"; \
		exit 1; \
	fi

.PHONY: echo-app-name
echo-app-name: ## Echo APP_NAME value (used in ci)
	@echo $(APP_NAME)

.PHONY: install-dev-requirements
install-dev-requirements: check-venv-is-activated ## Install DEV requirements
	@echo "+ $@"
	@echo "Installing local project dev requirements"
	pip install -r requirements_dev.txt

.PHONY: check-preflight
check-preflight:: ## Preflight/prerequisites checks
	@echo "+ $@"

.PHONY: check-all
check-all: clean lint test integration-test ## Reset cache and test everything
	@echo "+ $@"
