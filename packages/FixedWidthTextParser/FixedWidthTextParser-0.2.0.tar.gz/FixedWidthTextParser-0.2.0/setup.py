import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FixedWidthTextParser",
    version="0.2.0",
    author="Piotr Synowiec",
    author_email="psynowiec@gmail.com",
    description="Fixed width text parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mysiar/fixed-width-text-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
