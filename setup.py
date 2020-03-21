import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="registry_policy",
    version="1.0",
    author="Adrian Bool",
    author_email="aid.github@logic.org.uk",
    description="Microsoft Windows Registry Policy File (.pol) Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aid/registry_policy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
