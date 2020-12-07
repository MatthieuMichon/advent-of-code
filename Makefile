
venv:
	python -m venv venv

.PHONY: clean
clean:
	rm -rf venv
