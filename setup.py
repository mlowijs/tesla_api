import platform

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


packages = ["aiohttp", "mypy_extensions"]

dev = [
    "pytest",
    "pytest-mock",
    "pytest-monkeytype",
    "geopy",
    "pytest-asyncio",
    "pytest-cov",
]

if platform.python_version_tuple()[:2] <= ("3", "8"):
    dev.append("asynctest")

setup(
    name="tesla_api",
    version="2.0.1",
    author="M. Lowijs",
    author_email="mlowijs@gmail.com",
    description="API client for Tesla",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlowijs/tesla_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=packages,
    extras_require={"dev": dev},
)
