import os.path
from setuptools import setup, find_packages

# directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="findcrashedcodedeveloper",
    version="0.1.0",
    description="Find the developer responsible for crashed code from stack trace",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/karambir252/findcrashedcodedeveloper",
    author="Karambir Gahlot",
    author_email="karambir252@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests", "dummyfiles")),
    include_package_data=True,
    install_requires=[
        "graphqlclient", "requests"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        "console_scripts": [
            "findcrashedcodedeveloper=findcrashedcodedeveloper.__main__:main"
        ]
    },
)
