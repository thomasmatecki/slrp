import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slrp",
    version="0.0.0",
    author="Thomas Matecki",
    author_email="thomas.matecki@gmail.com",
    description="A Simple Parser Combinator Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasmatecki/slrp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
