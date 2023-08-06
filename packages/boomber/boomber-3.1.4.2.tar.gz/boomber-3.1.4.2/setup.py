import pathlib

from setuptools import setup

NAME = "boomber"
DESCRIPTION = "Открытый и бесплатный СМС бомбер"
URL = "https://github.com/doubledare704/b0mb3r"
EMAIL = ""
AUTHOR = "crinny"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "3.1.4.2"
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open("requirements.txt", encoding="utf-8") as f:
    REQUIRED = f.readlines()

try:
    with open("README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["boomber"],
    entry_points={
        "console_scripts": ["boomber=boomber.cli:main", "bomber=boomber.cli:main"]
    },
    install_requires=REQUIRED,
    extras_require={},
    package_data={"boomber": ["services/*", "app/*", "app/*/*", "app/static/*/*"]},
    license="Mozilla Public License 2.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Android",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
)
