import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dora-sl-evandro-teixeira-tatic", # Replace with your own username
    version="0.0.2",
    author="Evandro Teixeira",
    author_email="evandro.teixeira@tatic.net",
    description="Serverless Reader Poc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="git@10.10.0.13:bda/serverless-reader-poc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
