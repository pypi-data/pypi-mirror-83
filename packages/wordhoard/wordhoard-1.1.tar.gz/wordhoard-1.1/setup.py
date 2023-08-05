import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordhoard",
    version="1.1",
    author="John Bumgarner",
    author_email="wordhoardproject@gmail.com",
    description="lexicon searcher for textual analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnbumgarner/wordhoard",
    packages=setuptools.find_packages(),
    classifiers=["License :: OSI Approved :: MIT License", "Operating System :: OS Independent"],
    python_requires='>=3.6',
    install_requires=['bs4', 'lxml', 'requests', 'urllib3']
)
