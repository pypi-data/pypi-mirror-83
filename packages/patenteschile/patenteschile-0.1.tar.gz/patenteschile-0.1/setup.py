import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="patenteschile",
    version="0.1",
    author="Alejandro Farías",
    author_email="farias@8loop.cl",
    description="A small library for generate chilean car registration number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fariascl/patentechile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
