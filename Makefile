.DEFAULT_GOAL := help
PROG_NAME ?= yamkix
NAME := looztra/$(PROG_NAME)
CI_PLATFORM := circleci
GIT_SHA1 := $(shell git rev-parse --short HEAD)
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_DIRTY := $(shell git diff --quiet || echo '-dirty')
GIT_SHA1_DIRTY_MAYBE := ${GIT_SHA1}${GIT_DIRTY}
YAMKIX_VERSION := $(shell cat setup.py | grep version | cut -d "=" -f2 | cut -d "," -f 1 | cut -d"'" -f2)
TAG := ${YAMKIX_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_LATEST := "latest"
TAG_CIRCLECI := circleci-${YAMKIX_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_CIRCLECI_LATEST := "circleci-latest"
IMG := ${NAME}:${TAG}
IMG_CIRCLECI := ${NAME}:${TAG_CIRCLECI}
IMG_LATEST := ${NAME}:${TAG_LATEST}
IMG_LATEST_CIRCLECI := ${NAME}:${TAG_CIRCLECI_LATEST}

ifdef CIRCLE_BUILD_NUM
	CI_BUILD_NUMBER := "${CIRCLE_BUILD_NUM}"
else
	CI_BUILD_NUMBER := "N/A"
endif

.PHONY: eclint
eclint: ## Run eclint on files tracked by git
	@echo "+ $@"
	docker run --rm -v $(pwd):/app/code qima/eclint check $(git ls-files)

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	@echo "+ $@"

.PHONY: clean-build
clean-build: ## remove build artifacts
	@echo "+ $@"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "+ $@"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	@echo "+ $@"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: style
style: ## force style with black
	@echo "+ $@"
	black --line-length 79 tests $(PROG_NAME)

.PHONY: lint
lint: ## Run all linters
	@echo "+ $@"
	tox -e linters

.PHONY: tests
tests: unit-tests
	@echo "+ $@"

.PHONY: unit-tests
unit-tests: ## Run unit tests
	@echo "+ $@"
	tox -e py3

.PHONY: integration-tests
integration-tests: ## Run integration tests
	@echo "+ $@"
	bats tests.bats

.PHONY: all-tests
all-tests: unit-tests integration-tests ## Tests all
	@echo "+ $@"

.PHONY: all
all: lint all-tests ## lint and all tests
	@echo "+ $@"

.PHONY: dist
dist: ## Build python3 package
	@echo "+ $@"
	python setup.py bdist_wheel
	python setup.py sdist

.PHONY: dist-check
dist-check: ## Check the python3 package
	@echo "+ $@"
	twine check dist/$(PROG_NAME)-${YAMKIX_VERSION}-py2.py3-none-any.whl
	twine check dist/$(PROG_NAME)-${YAMKIX_VERSION}.tar.gz

.PHONY: dist-upload
dist-upload: ## Upload the python3 package to pypi
	twine upload dist/*

.PHONY: build
build: ## Build the docker image
	@echo "+ $@"
	docker image build \
		--build-arg CI_PLATFORM=${CI_PLATFORM} \
		--build-arg YAMKIX_VERSION=${YAMKIX_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		--build-arg CI_BUILD_NUMBER=${CI_BUILD_NUMBER} \
		-t ${IMG} -f exec${GIT_DIRTY}.Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif

.PHONY: build-circleci
build-circleci: ## Build the circleci docker image
	@echo "+ $@"
	docker image build \
		--build-arg CI_PLATFORM=${CI_PLATFORM} \
		--build-arg YAMKIX_VERSION=${YAMKIX_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		--build-arg CI_BUILD_NUMBER=${CI_BUILD_NUMBER} \
		-t ${IMG_CIRCLECI} -f circleci.Dockerfile .
	docker image tag ${IMG_CIRCLECI} ${IMG_LATEST_CIRCLECI}

.PHONY: push
push: ## Push the docker image with the sha1 tag
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG} (please check that you are logged in)"
	@docker image push ${IMG}
endif

.PHONY: push-latest
push-latest: ## Push the docker image with tag latest
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_LATEST} (please check that you are logged in)"
	@docker image push ${IMG_LATEST}
endif

.PHONY: push-circleci
push-circleci: ## Push the circleci docker image with the sha1 tag
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_CIRCLECI} (please check that you are logged in)"
	@docker image push ${IMG_CIRCLECI}
endif

.PHONY: push-circleci-latest
push-circleci-latest: ## Push the circleci docker image with tag latest
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_LATEST_CIRCLECI} (please check that you are logged in)"
	@docker image push ${IMG_LATEST_CIRCLECI}
endif

.PHONY: print-version
print-version:
	@echo ${YAMKIX_VERSION}

.PHONY: print-exec-version
print-exec-version:
	@echo ${TAG}

.PHONY: print-circleci-version
print-circleci-version:
	@echo ${TAG_CIRCLECI}

.PHONY: print-exec-latest
print-exec-latest:
	@echo ${TAG_LATEST}

.PHONY: print-circleci-latest
print-circleci-latest:
	@echo ${TAG_CIRCLECI_LATEST}

.PHONY: print-img-name
print-img-name:
	@echo ${NAME}

.PHONY: print-img-safe-name
print-img-safe-name:
	@echo ${NAME} | tr "/" "-"

.PHONY: help
help: ## Print help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
			| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-45s\033[0m %s\n", $$1, $$2}'
