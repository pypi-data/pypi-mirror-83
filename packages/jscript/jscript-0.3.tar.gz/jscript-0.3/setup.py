from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jscript",
    version="0.3",
    author="Silicon tech",
    long_description=long_description,
    long_description_content_type="text/markdown"
)