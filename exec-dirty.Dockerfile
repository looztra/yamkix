FROM python:3.7.2-slim-stretch

ARG CI_PLATFORM
LABEL io.nodevops.ci-platform ${CI_PLATFORM}
LABEL org.label-schema.schema-version "1.0"
LABEL org.label-schema.name "yamkix"
LABEL org.label-schema.description "yamkix packaged as a docker image"
LABEL org.label-schema.vcs-url "https://github.com/looztra/yamkix"
LABEL org.label-schema.vendor "looztra"
LABEL org.label-schema.docker.cmd.help "docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG help"
LABEL org.label-schema.docker.cmd "docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG -i input"

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
