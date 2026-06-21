PYTHON ?= python3

.PHONY: validate lint test compile package

validate:
	$(PYTHON) scripts/validate_repo.py validate

lint:
	$(PYTHON) scripts/validate_repo.py lint

test:
	$(PYTHON) scripts/validate_repo.py test

compile:
	$(PYTHON) scripts/compile_paper.py compile

package:
	$(PYTHON) scripts/compile_paper.py package
