import setuptools

with open("THORONDOR/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="THORONDOR",
    version="0.2.4.8",
    description="XANES package",
    author="David Simonne and Andrea Martini",
    author_email="contact@dsimonne.eu, andrea.martini@unito.it",
    url="https://pypi.org/project/THORONDOR/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    keywords = "XANES GUI lmfit widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
	include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
    "numpy",
    "pandas",
    "matplotlib",
    "ipywidgets",
    "scipy",
    "lmfit",
    "emcee",
    "corner",
    "xlrd",
    "numdifftools"]
)