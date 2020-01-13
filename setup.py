from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tesla_api",
    version="1.1.0",
    author="M. Lowijs",
    author_email="mlowijs@gmail.com",
    description="API client for Tesla",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlowijs/tesla_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"   
    ]
)
