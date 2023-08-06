import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="splogging",
    version="0.0.5",
    author="Stevie Py",
    author_email="st3v13py@gmail.com",
    description="Ease the creation of a logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steviepy/splogging",
    packages=setuptools.find_packages(),
    package_data={"splogging": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
