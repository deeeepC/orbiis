import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="orbiis",
    version="0.1.0",
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "cbitstruct",
        "ephem",
    ],
    author='Reece Palmer',
    author_email="reece@deepc.com",
    description="GNSS Processing Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deeeepC/orbiis",
    packages=setuptools.find_packages(),
    #package_data={
    #    "cssrlib": ["data/*.*", "tests/*.py"],
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)