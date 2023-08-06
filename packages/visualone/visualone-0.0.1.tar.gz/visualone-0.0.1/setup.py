import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualone",
    version="0.0.1",
    author="Visual One Technologies Inc.",
    author_email="contact@visualone.tech",
    description="Python API for VEDX.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://visualone.tech",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)