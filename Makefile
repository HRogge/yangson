PROJECT = yangson
VERSION = 1.2.0
.PHONY = tags deps install-deps test

tags:
	find $(PROJECT) -name "*.py" | etags -

deps:
	pip freeze > requirements.txt

install-deps:
	pip install -r requirements.txt

test:
	@py.test tests

release:
	git tag -a -m "Yangson release $(VERSION)" $(VERSION)
	rm -f dist/*
	python setup.py sdist
	python setup.py bdist_wheel

upload:
	twine upload dist/*
