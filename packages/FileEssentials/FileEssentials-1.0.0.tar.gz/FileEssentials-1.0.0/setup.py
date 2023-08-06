import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FileEssentials",
    version="1.0.0",
    author="DaRubyMiner360",
    author_email="darubyminer360@gmail.com",
    description="File Essentials is a package that contains all of the necessary functions for using files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/DaRubyMiner360/FileEssentials",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)