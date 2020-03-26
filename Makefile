all: clean cpyinst
cpyinst: cpywipe
	python setup.py install --user
pypyinst: pypywipe
	pypy3 setup.py install --user
clean:
	rm -rf *egg-info build dist
cpywipe:
	pip uninstall -y mocos_helper; pip uninstall -y mocos_helper; pip uninstall -y mocos_helper || true
pypywipe:
	pypy3 -m pip uninstall -y mocos_helper; pypy3 -m pip uninstall -y mocos_helper; pypy3 -m pip uninstall -y mocos_helper || true
wipe: cpywipe pypywipe
twine: clean
	python setup.py sdist
	twine upload dist/mocos_helper*.tar.gz
