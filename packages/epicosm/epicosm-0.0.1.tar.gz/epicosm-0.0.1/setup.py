import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epicosm",
    version="0.0.1",
    author="Alastair Tanner",
    author_email="alastair.tanner@bristol.ac.uk",
    description="Epidemiology of Cohort Social Media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DynamicGenetics/Epicosm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

