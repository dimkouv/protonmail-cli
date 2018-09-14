import setuptools

metadata = {}
with open("protonmail/metadata.py") as fh:
    exec(fh.read(), metadata)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=metadata["name"],
    version=metadata["__version__"],
    author=metadata["author_name"],
    author_email=metadata["author_email"],
    description=metadata["description"],
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    url=metadata["url"],
    python_requires='>=3',
    install_requires=[
        "beautifulsoup4",
        "selenium",
        "pyvirtualdisplay",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
