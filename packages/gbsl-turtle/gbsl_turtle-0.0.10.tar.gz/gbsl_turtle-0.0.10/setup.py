import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gbsl_turtle",
    version="0.0.10",
    author="Balthasar Hofer",
    author_email="lebalz@outlook.com",
    description="Typed default turtle for gym gsbl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GBSL-Informatik/gbsl_turtle",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
