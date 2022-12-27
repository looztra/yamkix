DOCKER_BINARY ?= docker
DOCKER_GUARD  := $(shell command -v ${DOCKER_BINARY} 2> /dev/null)
TAG           := ${YAMKIX_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_LATEST    := latest
IMG           := ${APP_NAME}:${TAG}
IMG_LATEST    := ${APP_NAME}:${TAG_LATEST}

.PHONY: check-docker
check-docker: ## Check if docker is installed 🐳
	@echo "+ $@"
ifndef DOCKER_GUARD
	$(error "docker (binary=${DOCKER_BINARY}) is not available please install it")
endif
	@echo "Found docker (binary=${DOCKER_BINARY}) (and that's a good news) 🐳"


.PHONY: docker-build
docker-build: check-docker ## ▶ Build the docker image 🐳
	@echo "+ $@"
ifndef YAMKIX_VERSION
	$(error "Please specify YAMKIX_VERSION")
endif
	docker image build \
		--build-arg YAMKIX_VERSION=${YAMKIX_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_REF=${GIT_REF_SAFE_NAME} \
		-t ${IMG} -f Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif
