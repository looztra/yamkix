FROM python:3.11-slim-bullseye

LABEL org.label-schema.schema-version="1.0" \
  org.label-schema.name="yamkix" \
  org.label-schema.description="yamkix packaged as a docker image" \
  org.label-schema.vcs-url="https://github.com/looztra/yamkix" \
  org.label-schema.vendor="looztra" \
  org.label-schema.docker.cmd.help="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG help" \
  org.label-schema.docker.cmd="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG -i input"

WORKDIR /app/code
COPY wait-for-pypi.sh /app/code
ENTRYPOINT ["yamkix"]
CMD ["--help"]
ARG GIT_SHA1
ARG GIT_BRANCH
LABEL org.label-schema.version=${YAMKIX_VERSION} \
  org.label-schema.vcs-ref=${GIT_SHA1} \
  io.nodevops.git-branch=${GIT_BRANCH}

ARG YAMKIX_VERSION
RUN chmod +x /app/code/wait-for-pypi.sh && \
  /app/code/wait-for-pypi.sh ${YAMKIX_VERSION} && \
  pip install --no-cache-dir yamkix==${YAMKIX_VERSION}
