DOCKER_BINARY ?= docker
DOCKER_GUARD  := $(shell command -v ${DOCKER_BINARY} 2> /dev/null)
TAG           := ${YAMKIX_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_LATEST    := latest
IMG           := ${NAME}:${TAG}
IMG_LATEST    := ${NAME}:${TAG_LATEST}

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
	docker image build \
		--build-arg YAMKIX_VERSION=${YAMKIX_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		-t ${IMG} -f exec.Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif
