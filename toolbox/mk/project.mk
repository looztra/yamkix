.PHONY: test-python-versions
test-python-versions: ## ▶ Run tests for all supported python versions
	@echo "Running tests for all supported python versions"
	@uv run tox run
