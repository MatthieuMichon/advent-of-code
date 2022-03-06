
venv:
	python -m venv venv
	python -m pip install --upgrade pip
	pip install pylint

.PHONY: clean
clean:
	rm -r venv
