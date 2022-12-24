
ASDF_IGNORE_TOOLS                   ?= not_empty_to_avoid_too_complex_command # | (pipe) separated list of tools that we want to ignore
STACK_TOOL_VERSIONS_FILENAME        ?= .tool-versions
ASDF_GUARD                          := $(shell command -v asdf 2> /dev/null)

.PHONY: check-asdf
check-asdf: ## Check if asdf is installed 🙉
	@echo "+ $@"
ifndef ASDF_GUARD
	$(error "asdf is not available please install it")
endif
	@echo "Found asdf 👌"

.PHONY: install-tools-asdf-plugins
install-tools-asdf-plugins: check-asdf ## Install asdf plugins for contributors
	@echo "+ $@"
	@echo "Checking asdf plugins"
	@echo
	@for plugin in $$(awk '{print $$1}' ${STACK_TOOL_VERSIONS_FILENAME} | grep -Ev '${ASDF_IGNORE_TOOLS}'); do \
		asdf plugin add $$plugin || true; \
	done

.PHONY: install-tools-with-asdf
install-tools-with-asdf: install-tools-asdf-plugins ## ▶ Install contrib tools with asdf ⚙️
	@echo "+ $@"
	@echo "Installing core stack tools"
	@echo
	@cat ${STACK_TOOL_VERSIONS_FILENAME}|grep -Ev '${ASDF_IGNORE_TOOLS}' | while read -r plugin version; do \
		asdf install $${plugin} $${version}; \
	done
