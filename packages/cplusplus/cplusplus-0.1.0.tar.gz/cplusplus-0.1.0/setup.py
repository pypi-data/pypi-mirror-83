from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cplusplus",
    version="0.1.0",
    author="Silicon tech",
    long_description=long_description,
    long_description_content_type="text/markdown"
)