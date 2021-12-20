FROM python:3.9-slim-buster

ARG CI_PLATFORM
LABEL io.nodevops.ci-platform=${CI_PLATFORM} \
  org.label-schema.schema-version="1.0" \
  org.label-schema.name="yamkix" \
  org.label-schema.description="yamkix packaged as a docker image" \
  org.label-schema.vcs-url="https://github.com/looztra/yamkix" \
  org.label-schema.vendor="looztra" \
  org.label-schema.docker.cmd.help="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG help" \
  org.label-schema.docker.cmd="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG -i input"

WORKDIR /app/code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY yamkix /

ENTRYPOINT ["/yamkix"]
CMD ["--help"]

ARG GIT_SHA1
ARG GIT_BRANCH
ARG CI_BUILD_NUMBER
ARG YAMKIX_VERSION
LABEL org.label-schema.version ${YAMKIX_VERSION}}
LABEL org.label-schema.vcs-ref ${GIT_SHA1}
LABEL io.nodevops.git-branch ${GIT_BRANCH}
LABEL io.nodevops.ci-build-number ${CI_BUILD_NUMBER}
