import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KLS-Statistics", # Replace with your own username
    version="0.0.1",
    author="ghostlypi",
    author_email="parth.iyer@gmail.com",
    description="A statistic package that works with Pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostlypi/Stats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)