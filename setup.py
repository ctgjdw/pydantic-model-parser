import os
import sys
import setuptools

VERSION = os.environ.get("CI_COMMIT_TAG", "0.0.0")

PYTHON_VER_REQ = f">={sys.version_info.major}.{sys.version_info.minor}"

with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

setuptools.setup(
    name="pydantic-model-parser",
    version=VERSION,
    description="A simple package to transform/map dictionaries, before parsing it into Pydantic.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=PYTHON_VER_REQ,
    packages=setuptools.find_packages(),
    use_pipfile=True,
)
