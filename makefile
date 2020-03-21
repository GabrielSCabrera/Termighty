main:
	@ echo "\033[1;3;32minstall dev build\033[m"
	@ pip3 install --editable .

remove:
	@ echo "\033[1;3;32muninstall dev build\033[m"
	@ pip3 uninstall .

clean-pyc:
	@ echo "\033[1;3;32mclean __pycache__\033[m"
	@ rm -f -r ./__pycache__/
	@ rm -f -r ./Termighty/__pycache__/
	@ rm -f -r ./Termighty/config/__pycache__/
	@ rm -f -r ./Termighty/data/__pycache__/
	@ rm -f -r ./Termighty/exceptions/__pycache__/
	@ rm -f -r ./Termighty/obj/__pycache__/
	@ rm -f -r ./Termighty/tests/__pycache__/
	@ rm -f -r ./Termighty/utils/__pycache__/

clean-build:
	@ echo "\033[1;3;32mclean build, dist, .egg-info\033[m"
	@ rm -f -r ./build/
	@ rm -f -r ./dist/
	@ rm -f -r ./*.egg-info

clean: clean-pyc clean-build

test: run_main clean-pyc

run_main:
	@ echo "\033[1;3;32mrun test\033[m"
	@ python3 ../main.py;
