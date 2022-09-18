from setuptools import setup, find_packages

dependencies = ("numpy","numba")

url = "https://github.com/GabrielSCabrera/Termighty"
setup(
    name="Termighty",
    packages=find_packages(where="source"),
    package_dir={"": "source"},
    include_package_data=True,
    package_data={"": ["data/*.json", "config.ini"]},
    version="0.0.1",
    description="Cross-Platform Terminal Coloring, Formatting, and Management Utilities.",
    author="Gabriel S. Cabrera",
    author_email="gabriel.sigurd.cabrera@gmail.com",
    url=url,
    download_url=url + "archive/v0.0.1.tar.gz",
    keywords=["terminal", "xterm", "gui", "windows", "linux"],
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
    ],
)
