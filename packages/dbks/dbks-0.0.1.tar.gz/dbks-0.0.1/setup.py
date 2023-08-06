import requests
from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as f:
        content = f.read()
        requirements = content.split("\n")
    return requirements


setup(
    name="dbks",
    version="0.0.1",
    author="Vincent Lam",
    author_email="vincent@lam.is",
    description="Databricks API client",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/vincentlam/dbks",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        dbks=dbks.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
