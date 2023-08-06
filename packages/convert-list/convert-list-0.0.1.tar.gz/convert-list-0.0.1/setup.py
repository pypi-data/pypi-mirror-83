import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convert-list",
    version="0.0.1",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Base for list with item conversion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/convert-list/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)