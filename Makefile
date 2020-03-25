all: clean
	pip uninstall -y mocos_helper; pip uninstall -y mocos_helper; pip uninstall -y mocos_helper || true
	python setup.py install --user
clean:
	rm -rf *egg-info build dist
