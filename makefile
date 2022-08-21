main: install

install:
	@ echo "\033[1;32minstall dev build\033[m"
	@ python -m pip install --editable .

uninstall:
	@ echo "\033[1;32muninstall dev build\033[m"
	@ python -m pip uninstall .

reinstall: uninstall install

clean-pyc:
	@ echo "\033[1;32mclean __pycache__ .pyc .nbi .nbc\033[m"
	@ find . -type d -name '*__pycache__' -exec rm -rf {} +
	@ find . -type d -name '*.pyc' -exec rm -rf {} +
	@ find . -type d -name '*.nbi' -exec rm -rf {} +
	@ find . -type d -name '*.nbc' -exec rm -rf {} +

clean-build:
	@ echo "\033[1;32mclean build, dist, .egg-info\033[m"
	@ rm -f -r ./build/
	@ rm -f -r ./dist/
	@ rm -f -r ./*.egg-info

clean: clean-pyc clean-build

test: test_wrap clean-pyc
test_wrap:
	@ echo "\033[1;32mrun test\033[m"
	@ python main.py --test;

help:
	@ python main.py -h;

push: clean-pyc
	@ echo "\033[1;32mpushing to github\033[m"
	@ git add .
	@ git commit -m "Automatic Backup"
	@ git push origin master

pull: clean-pyc
	@ echo "\033[1;32mpulling from github\033[m"
	@ git pull

clean-html:
	@ echo "\033[1;32mremoving all HTML files\033[m"
	@ find . -type d -name '*.html' -exec rm -rf {} +

pydoc: clean-pyc clean-html
	@ echo "\033[1;32mcreating pydoc HTML files\033[m"
	@ find . -type d -name '*.py' -exec pydoc -w {} +
	@ mkdir -p docs
	@ mv *.html ./docs

test: clean-pyc
	@ echo "\033[1;32mrunning all tests\033[m"
	@ python tests/main.py
