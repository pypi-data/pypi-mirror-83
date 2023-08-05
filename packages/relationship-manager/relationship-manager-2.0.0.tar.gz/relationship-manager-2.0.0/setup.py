import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="relationship-manager",
    version="2.0.0",
    description="Lightweight Object Database, manages relationships between classes",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abulka/relationship-manager",
    author="Andy Bulka",
    author_email="abulka@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # packages=find_packages(exclude=("tests","tests.examples")),
    packages=["relmgr"],
    include_package_data=True,
    install_requires=[],
    entry_points={
    },
)
