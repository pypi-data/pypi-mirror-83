import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nothing_anwarvic",
    version="1.0.2",
    author="Anwarvic",
    author_email="mohamedanwarvic@gmail.com",
    description="Nothing.. just nothing!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anwarvic/nothing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
