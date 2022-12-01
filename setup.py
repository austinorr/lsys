import re
from setuptools import setup, find_packages


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
    test_suite="lsys.tests",
    tests_require=test_requirements,
    entry_points={
        "console_scripts": [
            "lsys = lsys.cli:main",
        ],
    },
)
