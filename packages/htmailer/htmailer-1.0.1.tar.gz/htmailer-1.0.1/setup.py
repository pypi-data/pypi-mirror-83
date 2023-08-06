import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="htmailer",
    version="1.0.1",
    description="""Htmessage is simple extension of django's official 
                    EmailMessage. It is adapted to work with django 
                    templating engine or any templating engine adapted 
                    to work with django. """,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dino16m/htmailer",
    author="Dino16m",
    author_email="anselem16m@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["django"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True
    
)