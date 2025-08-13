.PHONY: test-python-versions
test-python-versions: ## ▶ Run tests for all supported python versions
	@echo "Running tests for all supported python versions"
	@uv run tox run

.PHONY: build-docs
build-docs: ## ▶ Build the documentation
	@echo "Building the documentation"
	@uv run mkdocs build

.PHONY: serve-docs
serve-docs: ## ▶ Serve the documentation
	@echo "Serving the documentation"
	@uv run mkdocs serve
