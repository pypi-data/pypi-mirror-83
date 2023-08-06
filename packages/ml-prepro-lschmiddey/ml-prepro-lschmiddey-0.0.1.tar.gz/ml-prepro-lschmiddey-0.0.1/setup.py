import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ml-prepro-lschmiddey", # Replace with your own username
    version="0.0.1",
    author="Lasse Schmidt",
    author_email="lasse.schmidt@live.de",
    description="Small package for preprocessing data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lschmiddey/ml_prepro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)