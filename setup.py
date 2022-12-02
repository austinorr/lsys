import re
from pathlib import Path

from setuptools import find_packages, setup


def search(substr: str, content: str):
    found = re.search(substr, content)
    if found:
        return found.group(1)
    return ""


with open("lsys/__init__.py", encoding="utf8") as f:
    content = f.read()
    version = search(r'__version__ = "(.*?)"', content)
    author = search(r'__author__ = "(.*?)"', content)
    author_email = search(r'__email__ = "(.*?)"', content)


requirements = ["numpy", "matplotlib"]

test_requirements = ["pytest>=3.1", "pytest-mpl>=0.8"]

setup(
    name="lsys",
    version=version,
    description="Create and visualize Lindenmayer systems",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url="https://github.com/austinorr/lsys",
    packages=find_packages(),
    include_package_data=False,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords=["l-systems", "lindenmayer", "fractal"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.8",
    test_suite="lsys.tests",
    tests_require=test_requirements,
    entry_points={
        "console_scripts": [
            "lsys = lsys.cli:main",
        ],
    },
)
