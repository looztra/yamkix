.PHONY: test-python-versions
test-python-versions: ## ▶ Run tests for all supported python versions
	@echo "Running tests for all supported python versions"
	@uv run tox run

.PHONY: build-docs
build-docs: ## ▶ Build the documentation
	@echo "Building the documentation"
	@uv run mkdocs build --site-dir generated/mkdocs/HEAD

.PHONY: serve-docs
serve-docs: ## ▶ Serve the documentation
	@echo "Serving the documentation"
	@uv run mkdocs serve

.PHONY: poe-integration-tests
poe-integration-tests: ## Run integration tests using poe
	@echo "+ $@"
	uv run poe pytest:integration

.PHONY: test-all
test-all: tests integration-tests poe-integration-tests test-python-versions ## ▶ Run all tests
	@echo "All tests completed successfully"

.PHONY: all-tests
all-tests: test-all ## ▶ Run all tests (alias for test-all)
