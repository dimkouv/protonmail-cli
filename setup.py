import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["selenium", "pyvirtualdisplay", "BeautifulSoup4"]

setuptools.setup(
    name="protonmail",
    version="0.0.6",
    author="dimkouv",
    install_requires=requirements,
    setup_requires=requirements,
    author_email="dimkouv@protonmail.com",
    description="Command line utility for https://protonmail.com",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/dimkouv/protonmail-cli",
    python_requires='>=3',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
