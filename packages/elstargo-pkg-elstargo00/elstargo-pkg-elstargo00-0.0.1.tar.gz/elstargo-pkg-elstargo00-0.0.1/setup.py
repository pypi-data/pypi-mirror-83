import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elstargo-pkg-elstargo00", # Replace with your own username
    version="0.0.1",
    author="Elstargo",
    author_email="tagam2707@gmail.com",
    description="FOR MY SELF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elstargo00/elstargo_package.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
