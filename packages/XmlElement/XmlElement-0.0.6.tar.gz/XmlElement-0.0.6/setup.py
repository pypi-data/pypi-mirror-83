import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XmlElement", 
    version="0.0.6",
    author="Roland Koller",
    author_email="info@ecmind.ch",
    description="A simpler XML writer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ecmind.ch/rk/xmlelement",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)