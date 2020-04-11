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

plot: plot_wrap clean-pyc
plot_wrap:
	@ echo "\033[1;3;32mrun plot\033[m"
	@ python3 main.py --plot;

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

clean-html: clean-pyc
	@ echo "\033[1;3;32mremoving all HTML files\033[m"
	@ rm -f -r ./*.html
	@ rm -f -r ./Termighty/*.html
	@ rm -f -r ./docs/*.html
	@ rm -f -r ./Termighty/config/*.html
	@ rm -f -r ./Termighty/data/*.html
	@ rm -f -r ./Termighty/backend/*.html
	@ rm -f -r ./Termighty/frontend/*.html
	@ rm -f -r ./Termighty/frontend/color_maps/*.html
	@ rm -f -r ./Termighty/samples/*.html
	@ rm -f -r ./Termighty/tests/*.html
	@ rm -f -r ./Termighty/tools/*.html
	@ rm -f -r ./Termighty/utils/*.html

pydoc: clean-pyc
	@ echo "\033[1;3;32mcreating pydoc HTML files\033[m"
	@ pydoc3 -w Termighty
	@ pydoc3 -w Termighty.backend
	@ pydoc3 -w Termighty.backend.Color_Fast
	@ pydoc3 -w Termighty.backend.Color
	@ pydoc3 -w Termighty.backend.Grid_Fast
	@ pydoc3 -w Termighty.backend.Grid
	@ pydoc3 -w Termighty.backend.Pixel_Fast
	@ pydoc3 -w Termighty.backend.Pixel
	@ pydoc3 -w Termighty.backend.Series_Fast
	@ pydoc3 -w Termighty.backend.Series
	@ pydoc3 -w Termighty.backend.Style_Fast
	@ pydoc3 -w Termighty.backend.Style
	@ pydoc3 -w Termighty.backend.Term
	@ pydoc3 -w Termighty.backend.Window
	@ pydoc3 -w Termighty.config
	@ pydoc3 -w Termighty.config.defaults
	@ pydoc3 -w Termighty.data
	@ pydoc3 -w Termighty.data.ANSI
	@ pydoc3 -w Termighty.data.RGB
	@ pydoc3 -w Termighty.data.types
	@ pydoc3 -w Termighty.frontend
	@ pydoc3 -w Termighty.frontend.Color_Map
	@ pydoc3 -w Termighty.frontend.Gradient
	@ pydoc3 -w Termighty.frontend.color_maps
	@ pydoc3 -w Termighty.frontend.color_maps.Linear_Map
	@ pydoc3 -w Termighty.samples
	@ pydoc3 -w Termighty.samples.logo
	@ pydoc3 -w Termighty.tests
	@ pydoc3 -w Termighty.tests.calibration
	@ pydoc3 -w Termighty.tests.Tester
	@ pydoc3 -w Termighty.tests.unit_tests
	@ pydoc3 -w Termighty.tools
	@ pydoc3 -w Termighty.tools.Painter
	@ pydoc3 -w Termighty.utils
	@ pydoc3 -w Termighty.utils.checkers
	@ pydoc3 -w Termighty.utils.format
	@ pydoc3 -w Termighty.utils.interpreters
	@ mv *.html ./docs
