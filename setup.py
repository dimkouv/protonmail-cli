import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protonmail",
    version="0.0.1",
    author="dimkouv",
    author_email="dimkouv@protonmail.com",
    description=" Command line utility for https://protonmail.com",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/dimkouv/protonmail-cli",
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
