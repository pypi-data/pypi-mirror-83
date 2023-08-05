"""metadata_utils installation script.
"""
import os
import re
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
long_description = description = ("Lightweight Metadata Support",)
try:
    long_description = open(os.path.join(here, "README.md")).read()
except:
    pass

# store version in the init.py
with open(
    os.path.join(os.path.dirname(__file__), "metadata_utils", "__init__.py")
) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)

requires = []
tests_require = [
    "six",
    "pytest",
]
testing_extras = tests_require + []

setup(
    name="metadata_utils",
    description="Lightweight Metadata Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    url="https://github.com/jvanasco/metadata_utils",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    zip_safe=False,
    keywords="web",
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
)
