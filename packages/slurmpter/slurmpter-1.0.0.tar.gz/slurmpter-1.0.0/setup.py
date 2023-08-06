from setuptools import setup
import os


def get_long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst')) as f:
        long_description = f.read()
    return long_description


VERSION = "1.0.0"

setup(
    name="slurmpter",
    version=VERSION,
    license="MIT",
    description="A package to build Slurm submit files of a workflow of jobs easily.",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    author="Isaac Chun Fung WONG",
    author_email="chunefung@gmail.com",
    url="https://gitlab.com/isaac-cfwong/slurmpter",
    python_requires=">=3.5",
    packages=["slurmpter"],
    install_requires=["graphviz", "pycondor"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
