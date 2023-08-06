import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hed_exceptions",
    version="0.0.4",
    author="Hrissimir",
    author_email="hrisimir.dakov@gmail.com",
    description="Set of custom exceptions aimed to reduce typing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hrissimir/hed_exceptions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
