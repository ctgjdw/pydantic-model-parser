import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pydantic-model-parser",
    version="1.0.1",
    description="A simple package to transform/map dictionaries, before parsing it into Pydantic.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ctgjdw/pydantic-model-parser",
    author="CTGJDW",
    author_email="gohchunteck@hotmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["model_parser"],
    install_requires=["pydantic >= 1.9.0", "pydash >= 5.0.0"],
)
