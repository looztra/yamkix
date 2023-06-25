FROM python:3.11-slim-bullseye

LABEL org.label-schema.schema-version="1.0" \
  org.label-schema.name="yamkix" \
  org.label-schema.description="yamkix packaged as a docker image" \
  org.label-schema.vcs-url="https://github.com/looztra/yamkix" \
  org.label-schema.vendor="looztra" \
  org.label-schema.docker.cmd.help="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG help" \
  org.label-schema.docker.cmd="docker run --rm -v $(pwd):/app/code looztra/yamkix:TAG -i input"
ENV PIP_ROOT_USER_ACTION=ignore \
  PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app/code
COPY wait-for-pypi.sh /app/code
ENTRYPOINT ["yamkix"]
CMD ["--help"]
ARG GIT_SHA1
ARG GIT_REF
ARG APP_VERSION
LABEL org.label-schema.version=${APP_VERSION} \
  org.label-schema.vcs-ref=${GIT_SHA1} \
  io.nodevops.git-ref=${GIT_REF}

RUN chmod +x /app/code/wait-for-pypi.sh && \
  /app/code/wait-for-pypi.sh ${APP_VERSION} yamkix && \
  pip install --no-cache-dir yamkix==${APP_VERSION}
