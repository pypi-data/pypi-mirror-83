import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chartree",
    version="0.0.8",
    author="bsmrvl",
    author_email="ben.j.somerville@icloud.com",
    description="Grow trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsmrvl/a-trees-character",
    packages=setuptools.find_packages(),
    install_requires=['numpy','IPython'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)