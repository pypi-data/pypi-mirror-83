import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="picrust", 
    version="0.0.0.1",
    author="Michael Edward Vinyard",
    author_email="vinyard@g.harvard.edu",
    description="Holds the pi together.",
    long_description="This package contains various functions for use with raspberry pi projects.",
    long_description_content_type="text/markdown",
    url="https://github.com/mvinyard/picrust",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

