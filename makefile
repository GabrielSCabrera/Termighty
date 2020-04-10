main: install

install:
	@ echo "\033[1;3;32minstall dev build\033[m"
	@ pip3 install --editable .

uninstall:
	@ echo "\033[1;3;32muninstall dev build\033[m"
	@ pip3 uninstall .

reinstall: uninstall install

clean-pyc:
	@ echo "\033[1;3;32mclean __pycache__\033[m"
	@ rm -f -r ./__pycache__/
	@ rm -f -r ./Termighty/__pycache__/
	@ rm -f -r ./Termighty/config/__pycache__/
	@ rm -f -r ./Termighty/data/__pycache__/
	@ rm -f -r ./Termighty/backend/__pycache__/
	@ rm -f -r ./Termighty/frontend/__pycache__/
	@ rm -f -r ./Termighty/frontend/color_maps/__pycache__/
	@ rm -f -r ./Termighty/samples/__pycache__/
	@ rm -f -r ./Termighty/tests/__pycache__/
	@ rm -f -r ./Termighty/tools/__pycache__/
	@ rm -f -r ./Termighty/utils/__pycache__/

clean-build:
	@ echo "\033[1;3;32mclean build, dist, .egg-info\033[m"
	@ rm -f -r ./build/
	@ rm -f -r ./dist/
	@ rm -f -r ./*.egg-info

clean: clean-pyc clean-build

test: test_wrap clean-pyc
test_wrap:
	@ echo "\033[1;3;32mrun test\033[m"
	@ python3 main.py --test;

calibrate: calibrate_wrap clean-pyc
calibrate_wrap:
	@ echo "\033[1;3;32mrun calibrate\033[m"
	@ python3 main.py --calibrate;

run: run_wrap clean-pyc
run_wrap:
	@ echo "\033[1;3;32mrun main\033[m"
	@ python3 main.py;

logo: logo_wrap clean-pyc
logo_wrap:
	@ echo "\033[1;3;32mrun logo\033[m"
	@ python3 main.py --logo;

help:
	@ python3 main.py -h;

push: clean-pyc
	@ echo "\033[1;3;32mpushing to github\033[m"
	@ git add .
	@ git commit -m "Automatic Backup"
	@ git push

pull: clean-pyc
	@ echo "\033[1;3;32mpulling from github\033[m"
	@ git pull
