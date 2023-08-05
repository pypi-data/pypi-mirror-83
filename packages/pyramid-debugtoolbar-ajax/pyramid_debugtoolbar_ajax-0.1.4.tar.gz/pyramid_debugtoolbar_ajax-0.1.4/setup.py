"""pyramid_debugtoolbar_ajax installation script.
"""
import os
import re
from setuptools import setup
from setuptools import find_packages

here = os.path.dirname(__file__)

long_description = description = "Ajax support for pyramid_debugtoolbar"
with open(os.path.join(here, "README.md")) as r_file:
    long_description = r_file.read()
    
# store version in the init.py
with open(os.path.join(here, "pyramid_debugtoolbar_ajax", "__init__.py")) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)


requires = [
    "pyramid_debugtoolbar>=4.0",
]
tests_require = [
    "pytest",
    "pyramid",
]
testing_extras = tests_require + []

setup(
    name="pyramid_debugtoolbar_ajax",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_debugtoolbar_ajax",
    version=VERSION,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="web pyramid ajax debug",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
)
