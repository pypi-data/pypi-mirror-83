from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='customner',
      version='0.0.4',
      description='Custom Name Entity Recognition Data Preparation Library for Medical Dataset',
      py_modules=["customner"],
      package_dir={'':'Package'},
      long_description=long_description,
      long_description_content_type="text/markdown",
      )