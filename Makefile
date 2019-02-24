NAME := looztra/yamkix
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

.PHONY: build dist clean

eclint:
	docker run --rm -v $(pwd):/app/code qima/eclint check $(git ls-files)

python-checks:
	pylama

clean:
	rm -rf dist

dist:
	python setup.py bdist_wheel
	python setup.py bdist_egg

dist-check:
	twine check dist/yamkix-${YAMKIX_VERSION}-py2-none-any.whl
	twine check dist/yamkix-${YAMKIX_VERSION}-py2.7.egg

dist-upload:
	twine upload dist/*

build:
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

build-circleci:
	docker image build \
		--build-arg CI_PLATFORM=${CI_PLATFORM} \
		--build-arg YAMKIX_VERSION=${YAMKIX_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		--build-arg CI_BUILD_NUMBER=${CI_BUILD_NUMBER} \
		-t ${IMG_CIRCLECI} -f circleci.Dockerfile .
	docker image tag ${IMG_CIRCLECI} ${IMG_LATEST_CIRCLECI}

push:
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG} (please check that you are logged in)"
	@docker image push ${IMG}
endif

push-latest:
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_LATEST} (please check that you are logged in)"
	@docker image push ${IMG_LATEST}
endif

push-circleci:
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_CIRCLECI} (please check that you are logged in)"
	@docker image push ${IMG_CIRCLECI}
endif

push-circleci-latest:
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_LATEST_CIRCLECI} (please check that you are logged in)"
	@docker image push ${IMG_LATEST_CIRCLECI}
endif

print-exec-version:
	@echo ${TAG}

print-circleci-version:
	@echo ${TAG_CIRCLECI}

print-exec-latest:
	@echo ${TAG_LATEST}

print-circleci-latest:
	@echo ${TAG_CIRCLECI_LATEST}

print-img-name:
	@echo ${NAME}

print-img-safe-name:
	@echo ${NAME} | tr "/" "-"
