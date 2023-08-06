import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydesign",
    version="0.0.1",
    author="Syed Jafer",
    author_email="contact.syedjafer@gmail.com",
    description="Design Patterns implemented in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syedjafer/PyDesign",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)