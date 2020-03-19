main:
	@ echo "install dev build"
	@ pip3 install --editable .

uninstall:
	@ echo "uninstall dev build"
	@ pip3 uninstall .

clean-pyc:
	@ echo "clean __pycache__"
	@ rm -f -r ./repo/__pycache__/

clean-build:
	@ echo "clean build, dist, .egg-info"
	@ rm -f -r ./build/
	@ rm -f -r ./dist/
	@ rm -f -r ./*.egg-info

clean: clean-pyc clean-build

test: clean-pyc
	@ echo "run test"
	@ python3 ../main.py
