# following https://packaging.python.org/tutorials/packaging-projects/

# https://packaging.python.org/key_projects/#setuptools
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typelint",
    version="0.0.1",
    author="David Jones",
    author_email="drj@pobox.com",
    description="List typehints found in Python source code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/drj11/typelint",
    package_dir={"":"code"},
    py_modules=["typelint"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
