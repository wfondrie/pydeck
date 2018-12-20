import setuptools
import pydeck

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydeck",
    version=pydeck.__version__,
    package_data={"pydeck":["css/*.css"]},
    author="William E Fondrie",
    author_email="fondriew@gmail.com",
    description="Painlessly make remark slide decks with Python and markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wfondrie/pydecks",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Topic :: Multimedia :: Graphics :: Presentation"]
)
