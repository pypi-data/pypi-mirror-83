import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "journal-styles",
    version = "1.0rc1",
    author = "Iacopo Torre",
    author_email = "iacopo.torre@icfo.eu",
    description = "Package for producing consistent figure dimensions for scientific journals",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/itorre/journal-styles", 
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ],
    include_package_data = True,
    package_data = {'': ['styles/*']},
    python_requires = '>=3'
)