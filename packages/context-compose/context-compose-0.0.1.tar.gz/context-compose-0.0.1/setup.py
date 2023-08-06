import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="context-compose",
    version="0.0.1",
    author="Jack Riches",
    author_email="jackriches@gmail.com",
    description="Compose context managers from a sequence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackric/context_compose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
