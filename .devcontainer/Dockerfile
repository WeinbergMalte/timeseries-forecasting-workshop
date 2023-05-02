# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.231.6/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Poetry
ARG POETRY_VERSION="none"
RUN if [ "${POETRY_VERSION}" != "none" ]; then su vscode -c "umask 0002 && pip3 install poetry==${POETRY_VERSION}"; fi
