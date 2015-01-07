packages=command

.PHONY: test
test:
	NOSE_COVER_PACKAGE="$(packages)" nosetests -v

.PHONY: clean
clean:
	find . -name "*.pyc" -exec rm {} \;
