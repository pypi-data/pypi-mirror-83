from setuptools import setup, find_packages

setup(
    name="CoStrOb",
    version="0.0.1",
    description="time multiple tasks for optimized usage of recourses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fabian Becker",
    author_email="fab.becker@protonmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)
