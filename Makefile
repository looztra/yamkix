APP_NAME ?= yamkix

include tooling/mk/common.mk
include tooling/mk/actionlint.mk
include tooling/mk/pre-commit.mk

# include shared mk
include tooling/mk/python-poetry-venv.mk
include tooling/mk/python-poetry-app.mk
