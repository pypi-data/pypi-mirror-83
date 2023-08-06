import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtfuncs",
    version="0.0.1",
    author="Vladimir Elizarov",
    author_email="vladimirelizarov89@gmail.com",
    description="Useful functions to work with date and time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p0m1d0rka/dtfuncs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)