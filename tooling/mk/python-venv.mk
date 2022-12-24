VENV_DIR                ?= .venv
VENV_PYTHON3            := python3
PYTHON3_GUARD           := $(shell command -v ${VENV_PYTHON3} 2> /dev/null)
VENV_EXISTS             := $(shell ls -d $(VENV_DIR) 2> /dev/null)
VENV_ACTIVATED          := $(shell echo $(VIRTUAL_ENV) 2> /dev/null)
VENV_ACTIVATE_FISH_CMD  := source $(VENV_DIR)/bin/activate.fish
VENV_ACTIVATE_OTHER_CMD := source $(VENV_DIR)/bin/activate
PIP_CONF_PATH           := ~/.config/pip/pip.conf
PYPIRC_PATH             := ~/.pypirc
PYPIRC_EXISTS           := $(shell ls $(PYPIRC_PATH) 2> /dev/null)
PYPIRC_CONTENT          ?= "[distutils]\nindex-servers = \n    cpe-common-xix9-python\n\n[cpe-common-xix9-python]\nrepository: $(GAR_PYTHON_URL)/\n"
PIP_TOOLS_GUARD         := $(shell command -v pip-compile 2> /dev/null)
CUSTOM_COMPILE_COMMAND  ?= "make update-requirements-file"
PIP_TOOLS_ARGS          ?=
PIP_FIXED_VERSION       ?=

.PHONY: check-python3
check-python3: ## Check if python3 is installed 🐍
	@echo "+ $@"
ifndef PYTHON3_GUARD
	$(error "python3 is not available please install it")
endif
	@echo "Found ${VENV_PYTHON3} (and that's a good news)"

.PHONY: check-venv-exists
check-venv-exists: ## Check if venv is created 🙉
	@echo "+ $@"
ifndef VENV_EXISTS
	$(error "no venv dir [$(VENV_DIR)] found, please create it first with 'make setup-venv'")
endif
	@echo "Found venv (and that's a good news)"

.PHONY: check-pip-tools
check-pip-tools: check-venv-is-activated ## Check if pip-tools is installed 🐍
	@echo "+ $@"
ifndef PIP_TOOLS_GUARD
	@echo "pip-tools does not seem installed, installing it"
	@pip install --upgrade pip-tools
endif
	@echo "Found pip-tools (and that's a good news)"

.PHONY: setup-venv
setup-venv: check-python3 ## ▶ Setup a virtual env for running our python goodness 🎃
	@echo "+ $@"
	${VENV_PYTHON3} -m venv $(VENV_DIR) --upgrade-deps
ifdef PIP_FIXED_VERSION
	@echo "Forcing pip version to [$(PIP_FIXED_VERSION)]"
	${VENV_DIR}/bin/python -m pip install --upgrade "pip==$(PIP_FIXED_VERSION)" --disable-pip-version-check
endif

.PHONY: delete-venv
delete-venv: ## ▶ Delete venv
	@echo "+ $@"
	@if [ -d $(VENV_DIR) ]; then \
		echo "Deleting directory [$(VENV_DIR)]"; \
		rm -rf $(VENV_DIR); \
	else \
		echo "Nothing to do, directory [$(VENV_DIR)] does not exist"; \
	fi

.PHONY: venv
venv: setup-venv

.PHONY: activate-venv
activate-venv: check-python3 check-venv-exists ## Activate venv for the current shell ✨
	@echo "+ $@"
	@echo "Activating venv for shell [$(CURRENT_SHELL)]"
	@echo "please exec the current command: "
	@echo "------------>"
	@if [[ "$(CURRENT_SHELL)" == "fish" ]]; then \
		echo $(VENV_ACTIVATE_FISH_CMD); \
	else \
		echo $(VENV_ACTIVATE_OTHER_CMD); \
	fi
	@echo "<------------"

.PHONY: echo-venv-activate-cmd
echo-venv-activate-cmd: SHELL := $(WHICH_BASH)
echo-venv-activate-cmd: ## ▶ Echo the command to use to activate the venv
	@if [[ "$(CURRENT_SHELL)" == "fish" ]]; then \
		echo $(VENV_ACTIVATE_FISH_CMD); \
	else \
		echo $(VENV_ACTIVATE_OTHER_CMD); \
	fi

.PHONY: check-venv-is-ready
check-venv-is-ready: check-venv-is-activated check-gcloud-adc
	echo "+ $@"

.PHONY: check-venv-is-activated
check-venv-is-activated: ## Check if venv is activated 👻
	@echo "+ $@"
ifndef VENV_ACTIVATED
	$(error "venv does not seem to be activated, please activate it with 'make activate-venv'")
endif
	@echo "venv activated (and that's a good news)"
	@echo "Running venv from [${VIRTUAL_ENV}]"

.PHONY: check-requirements
check-requirements: check-venv-is-activated ## Check if requirements are met
	@echo "+ $@"
	@if python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))"; then \
		echo "All requirements are already met 👌"; \
	else \
		echo "⛈️  ERROR ⛈️: requirements.txt does not seem to be satisfied, please run 'make install-requirements' again" ;\
	fi

.PHONY: install-requirements
install-requirements: check-venv-is-activated ## ▶ Install python requirements 🧰
	@echo "+ $@"
	pip install -r requirements.txt

.PHONY: exit-venv
exit-venv: check-venv-is-activated ## Exit venv (deactivate) 👋
	@echo "+ $@"
	@echo "Please exec the command:"
	@echo "deactivate"

.PHONY: delete-pip-conf
delete-pip-conf: ### Delete pip.conf if it exists
	@echo "+ $@"
	@if [ -f $(PIP_CONF_PATH) ]; then \
		echo "Found file [$(PIP_CONF_PATH)], deleting it"; \
		rm $(PIP_CONF_PATH); \
	else \
		echo "File [$(PIP_CONF_PATH)] not found, doing nothing"; \
	fi

.PHONY: setup-pypirc
setup-pypirc: ## setup pypirc for GAR
	@echo "+ $@"
ifndef PYPIRC_EXISTS
	@echo "File [$(PYPIRC_PATH)] does not exist"
	@echo "Creating it"
	@printf $(PYPIRC_CONTENT) > $(PYPIRC_PATH)
	@echo "File [$(PYPIRC_PATH)] now contains:"
	@cat $(PYPIRC_PATH)
else
	@echo "File [$(PYPIRC_PATH)] exists"
	@echo "**Not overwriting it**"
	@echo "Current content"
	@echo "--------->"
	@cat $(PYPIRC_PATH)
	@echo "<---------"
	@echo "Make sure it contains the lines:"
	@echo "--------->"
	@printf $(PYPIRC_CONTENT)
	@echo "<---------"
endif

.PHONY: delete-pypirc
delete-pypirc: ### Delete pypirc if it exists
	@echo "+ $@"
	@if [ -f $(PYPIRC_PATH) ]; then \
		echo "Found file [$(PYPIRC_PATH)], deleting it"; \
		rm $(PYPIRC_PATH); \
	else \
		echo "File [$(PYPIRC_PATH)] not found, doing nothing"; \
	fi

.PHONY: check-gar-prerequisites
check-gar-prerequisites: SHELL := $(WHICH_BASH)
check-gar-prerequisites: ## Check that prerequisites are OK if GAR is needed
	@echo "+ $@"
	@echo "(pwd is $(PWD))"
ifndef BYPASS_GAR
	@echo "GAR access is requested (because BYPASS_GAR is not set)"
	@if ! pip freeze | grep keyrings.google-artifactregistry-auth; then \
		echo "Required package 'keyrings.google-artifactregistry-auth' is not available"; \
		echo -e "\e[31mplease run [make install-requirements] from the root of the repository\e[0m"; \
		echo; \
		exit 1; \
	else \
		echo "Required package 'keyrings.google-artifactregistry-auth' is available, you can go on"; \
	fi
else
	@echo "GAR access is NOT requested (because BYPASS_GAR is set to [$(BYPASS_GAR)])"
endif


.PHONY: update-requirements-file
update-requirements-file: SHELL := $(WHICH_BASH)
update-requirements-file: check-venv-is-activated check-gar-prerequisites check-pip-tools ## ▶ Update requirements.txt from requirements.in or setup.py 🧰
	@echo "+ $@"
	@if [ -f requirements.in -o -f setup.py -o -f pyproject.toml ]; then \
		declare -a pip_tools_args=(); \
		if [ -z "$(BYPASS_GAR)" ]; then \
			pip_tools_args+=(--extra-index-url=${GAR_PYTHON_URL}/simple/); \
		fi; \
		if [ -n "$(PIP_TOOLS_ARGS)" ]; then \
			pip_tools_args+=(${PIP_TOOLS_ARGS}); \
		fi; \
		if [ -f setup.py ]; then \
			echo "Found a [setup.py] file, using it to update requirements.txt"; \
			src_file=setup.py; \
		elif [ -f pyproject.toml ]; then \
			echo "Found a [pyproject.toml] file, using it to update requirements.txt"; \
			src_file=pyproject.toml; \
		else \
			echo "No [setup.py] and no [pyproject.toml], let's rely on [requirements.in] file, using it to update requirements.txt"; \
			src_file=requirements.in; \
		fi; \
		CUSTOM_COMPILE_COMMAND=$(CUSTOM_COMPILE_COMMAND) pip-compile $${pip_tools_args[@]} $${src_file} > requirements.txt; \
	else \
		echo "No requirements.in file, skipping."; \
	fi

.PHONY: check-requirements-constraints
check-requirements-constraints: SHELL := $(WHICH_BASH)
check-requirements-constraints: check-find check-venv-is-activated check-pip-tools ## ▶ Check if all requirements are compatible between themselves
	@echo "+ $@"
	pip-compile --dry-run $$($(FIND_CMD) . -type f -name requirements.txt | grep -Ev "generated|test-assets") --output-file=-

.PHONY: install-all-requirements
install-all-requirements: SHELL := $(WHICH_BASH)
install-all-requirements: check-find check-venv-is-activated check-pip-tools ## ▶ Install all requirements in a single command (requires make install-requirements)
	@echo "+ $@"
	pip-sync $$($(FIND_CMD) . -type f -name requirements.txt | grep -Ev "generated|test-assets")

.PHONY: update-all-requirements-files
update-all-requirements-files: check-find check-venv-is-activated ## ▶ Update all requirements files
	@echo "Updating [all] requirements.txt..."
	$(FIND_CMD) -L . -type f -name requirements.txt -not -path "**/generated/*" -not -path "**/test-assets*" \( -print -a -execdir bash -c "if test -f Makefile; then make update-requirements-file; else echo 'No Makefile found, skipping'; fi" \; -o -quit \)

.PHONY: check-local-cpe-common-usage
check-local-cpe-common-usage: ## Check that cpe-common is required locally (and not from GAR)
	@echo "+ $@"
	@if grep "cpe-common==" requirements.txt; then \
		echo -e "\e[31m[cpe-common] appears in the [requirements.txt] file but it should not\e[0m"; \
		echo -e "\e[31mPlease remote the line manually.\e[0m"; \
		echo ;\
		exit 1; \
	fi
