import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epricepy", # Replace with your own username
    version="0.1",
    author="Christ Oliver Lloyd",
    author_email="christlloyd.lloyd@gmail.com",
    description="This package alows the user to get selected e-commerce product's title and price as tuple according to the user's input url.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zero-Autumn/eprice-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['lxml', 'requests','beautifulsoup4'],
    python_requires='>=3.6',
)
