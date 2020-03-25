all: clean cpyinst pypyinst
cpyinst:
	pip uninstall -y mocos_helper; pip uninstall -y mocos_helper; pip uninstall -y mocos_helper || true
	python setup.py install --user
pypyinst:
	pypy3 -m pip uninstall -y mocos_helper; pypy3 -m pip uninstall -y mocos_helper; pypy3 -m pip uninstall -y mocos_helper || true
	pypy3 setup.py install --user
clean:
	rm -rf *egg-info build dist
