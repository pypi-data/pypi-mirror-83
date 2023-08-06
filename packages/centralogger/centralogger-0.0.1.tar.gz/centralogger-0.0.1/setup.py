import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="centralogger",
    version="0.0.1",
    author="Behan Remoshan BENET RUBAN",
    author_email="reevoremo@gmail.com",
    description="Log handler to deliver logs to multiple end points",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reevoremo/centralogger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
