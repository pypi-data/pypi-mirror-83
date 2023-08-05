import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MapColoniesJSONLogger", 
    version="0.0.12",
    author="MapColonies",
    author_email="mapcolonies@gmail.com",
    description="A JSON logger for map colonies project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/json-logger",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=[
        "python-json-logger >= 2.0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
