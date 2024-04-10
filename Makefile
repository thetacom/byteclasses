.PHONY: clean lint bandit black check mypy pycodestyle ruff test build api-docs docs
PKG := byteclasses

SRC_DIR := $(PKG)
ARTIFACT_DIR := dist
TEST_DIR := tests
DOCS_DIR := docs
DOCS_SRC_DIR := $(DOCS_DIR)
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
DOCS_SRC_FILES := $(wildcard $(DOCS_SRC_DIR)/*.rst)
DOCS_SRC_FILES += $(wildcard $(DOCS_SRC_DIR)/*.md)
DOCS_HTML_DIR := $(BUILD_DIR)/html

build: .venv
	@echo "*****Packaging $(PKG)*****"
	@poetry build -n

.venv:
	@echo "*****Creating Python Virtual Environment*****"
	@poetry install -q -n

clean:
	@rm -rf $(BUILD_DIR) $(DOCS_BUILD_DIR) .mypy_cache .pytest_cache ./*/__pycache__ reports .coverage

check: .venv
	@echo "*****Pre-Commit Checks*****"
	@pre-commit run --all-files

lint: bandit black ruff pydocstyle pycodestyle

analyze: pylint mypy

bandit: .venv
	@echo "*****Bandit*****"
	bandit -r --exit-zero $(SRC_DIR)

bandit_ci: .venv
	bandit -r -v -f xml -o reports/bandit.xml $(SRC_DIR)

black: .venv
	@echo "*****Black*****"
	@black --check $(SRC_DIR)

mypy: .venv
	@echo "*****Mypy*****"
	@mypy --pretty --disable-error-code import $(SRC_DIR)

pydocstyle: .venv
	@echo "*****Pydocstyle*****"
	@pydocstyle $(SRC_DIR)

pylint: .venv
	@echo "*****Pylint*****"
	@pylint $(SRC_DIR)

ruff: .venv
	@echo "*****Ruff*****"
	@ruff check --config pyproject.toml --show-source -e .

test: .venv
	@echo "*****Pytest*****"
	@pytest

api-docs:
	sphinx-apidoc --ext-autodoc --ext-doctest --ext-todo --ext-coverage --ext-githubpages -o $(DOCS_SRC_DIR)/api $(SRC_DIR)

docs: $(DOCS_SRC_FILES)
	sphinx-build -b html $(DOCS_SRC_DIR) $(DOCS_HTML_DIR)
