
import setuptools

name = 'pycybos'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version="0.0.0",
    author="innovata sambong",
    author_email="iinnovata@gmail.com",
    description=f"Wrapper for 대신증권 CYBOS Plus Open API",
    long_description="",
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/{name}",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
