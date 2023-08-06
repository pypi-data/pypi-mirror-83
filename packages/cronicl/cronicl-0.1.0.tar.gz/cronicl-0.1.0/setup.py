from setuptools import setup, find_packages

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='cronicl',
   version='0.1.0',
   description='cronicl is a simple data processing library',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Joocer',
   author_email='justin.joyce@joocer.com',
   packages=find_packages(),
   url="https://github.com/joocer/cronicl",
   install_requires=['networkx', 'flask']
)