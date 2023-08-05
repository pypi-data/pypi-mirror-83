import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hello-ron-pkg",
    version="0.0.1",
    author="Ron Snir",
    author_email="ron.snir@klarna.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stash.int.klarna.net/projects/PLUSUW/repos/python-project-test/browse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)