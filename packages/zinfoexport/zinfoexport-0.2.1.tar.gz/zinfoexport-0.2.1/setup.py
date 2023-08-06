import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read() 

setuptools.setup( 
    name="zinfoexport",
    version = "0.2.1",
    author = "Tobias Cadée",
    author_email = "t.cadee@hhsk.nl",
    description="Package to extract data from z-info (historian)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://bitbucket.org/TobiasCadee/z-info_export",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires = ">=3.6"
)