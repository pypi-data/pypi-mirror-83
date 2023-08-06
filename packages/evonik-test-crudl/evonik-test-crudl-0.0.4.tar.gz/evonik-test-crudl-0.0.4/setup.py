import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evonik-test-crudl",
    version="0.0.4",
    author="Benjamin Schiller",
    author_email="benjamin.schiller@evonik.com",
    description="Helpers for testing CRUDL-like APIs, e.g., REST and GQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://evodl.visualstudio.com/evonik-test-crudl",
    #packages=setuptools.find_packages(),
    packages=setuptools.find_namespace_packages(include=['evonik.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "evonik-dummy>=0.0.11",
        "pytest>=6.0.1"
    ],
)
