PACKAGES=command

.PHONY: test
test:
	NOSE_COVER_PACKAGE="$(PACKAGES)" nosetests -v

.PHONY: clean
clean:
	find . -name "*.pyc" -exec rm {} \;
