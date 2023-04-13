from setuptools import setup, find_packages
# from Cython.Build import cythonize

dependencies = ["numpy"]

url = "https://github.com/GabrielSCabrera/Termighty"

with open("README.md", 'r') as fs:
    long_description = fs.read()

setup(
    name="Termighty",
    packages=find_packages(where="source"),
    package_dir={"": "source"},
    include_package_data=True,
    package_data={"": ["data/*.json", "config.ini"]},
    version="3.0.3",
    description="Cross-Platform Terminal Coloring, Formatting, and Management Utilities.",
    long_description=long_description,
    author="Gabriel S. Cabrera",
    author_email="gabriel.sigurd.cabrera@gmail.com",
    url=url,
    download_url=url + "archive/v3.0.3.tar.gz",
    keywords=["terminal", "xterm", "gui", "windows", "linux"],
    install_requires=dependencies,
    # ext_modules=cythonize(["source/termighty/utils/key_processor.pyx"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
    ],
)
