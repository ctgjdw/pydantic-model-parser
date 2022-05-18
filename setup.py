import os
import setuptools

VERSION = os.environ.get("CI_COMMIT_TAG", "0.0.0")
with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

with open("requirements.txt", "r", encoding="utf-8") as file:
    REQUIREMENTS = [
        line.strip() for line in file.readlines() if line and not line.startswith("#")
    ]

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
    install_requires=REQUIREMENTS,
    python_requires=">=3.8",
    packages=setuptools.find_packages(),
    use_pipfile=True,
)
