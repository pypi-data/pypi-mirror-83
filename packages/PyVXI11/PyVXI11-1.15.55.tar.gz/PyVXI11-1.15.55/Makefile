#!make
# -*- coding:utf-8 -*-
#
.PHONY: update_hgstamp
.phony:distclean checkin release cVXI11 build device_clear all clean readme install

all:clean cVXI11 vxi11scan vxi11_device_clear

CC=/usr/bin/clang
CXX=/usr/bin/clang++

# from https://www.mercurial-scm.org/wiki/VersioningWithMake
#HGVERSION:= $(shell hg parents --template 'hgid: {node|short}')
HGVERSION:= $(shell hg parents --template 'HGTagShort = \\\"{latesttag}.{latesttagdistance}\\\"')
VERSION:= $(shell python3 setup.py --version)

hgstamp.py: update_hgstamp
	[ -f $@ ] || touch $@
	echo $(HGVERSION) | cmp -s $@ - || echo $(HGVERSION) > $@
#

distclean:
	-rm cVXI11-*.{c,h,cpp}
	-rm cVXI11_*.{c,h,cpp}
	-rm VXI11_*.{c,h}
	-rm VXI11.h
	-rm getifaddrs.{c,h,cpp}
	-rm ./build/bdist.*

checkin :
	-hg ci -m "before release $(HGVERSION)"
	hg kwexpand
	make hgstamp.py

release: distclean
	make readme
	make hgstamp.py
	hg bookmark -i "release $(HGVERSION)"
	python3 setup.py sdist

upload:
	python3 -m twine upload  dist/PyVXI11-$(VERSION).tar.gz

#python3 -m twine upload  dist/PyVXI11-$(shell hg parents --template '{latesttag}.{latesttagdistance}').tar.gz

cVXI11: setup.py hgstamp.py
	python setup.py clean
	-python3 setup.py clean
	python setup.py build
	-python3 setup.py build

install:
	rm -r ./build/bdist.*
	python3 setup.py install
	rm -r ./build/bdist.*
	python2 setup.py install

build: cVXI11

vxi11scan:vxi11_scan
	ln vxi11_scan vxi11scan

vxi11_scan:vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_scan

device_clear:vxi11_device_clear

vxi11_device_clear: misc/vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g -I . misc/vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_device_clear

readme: README.rst
	/usr/local/bin/pandoc -t plain -o README.txt README.rst
	/usr/local/bin/pandoc -t html -o README.html README.rst
	/usr/local/bin/pandoc -t markdown -o README.md README.rst

sdist:
	python3 setup.py sdist

