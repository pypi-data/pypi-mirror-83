# vim: set noexpandtab ts=4 sw=4:

# There must be a nicer way to do this
PYTHONARCH=$(shell python utils/pythonarch)
PYTHONARCH3=$(shell python3 utils/pythonarch)

BINS=$(shell python setup.py --list-scripts)

DEVELVERSION ?= 0.DEVEL.$(shell date +%Y%m%d%H%M)
RELEASEVERSION ?= $(DEVELVERSION)

all: all-python3

doc: doc-html

doc-html: all
	python3 setup.py build_sphinx

clean:
	python3 setup.py clean
	# Stupid python setuptools don't even clean the build directory
	rm -fr build
	rm -fr doc/build
	rm -fr sails.egg-info

test3: all-python3
	py.test-3 -c setup.cfg sails

testv3: all-python3
	py.test-3 -c setup.cfg -v sails

all-python3:
	python3 setup.py build

install-python3: all-python3
	python3 setup.py install --prefix=$(DESTDIR)/usr

spell:
	codespell -s --ignore-words=ignore_words.txt `find . -type f -name \*.py`

.PHONY: clean doc doc-html all all-python3 test3 testv3 pythonarch install-python3 codespell
