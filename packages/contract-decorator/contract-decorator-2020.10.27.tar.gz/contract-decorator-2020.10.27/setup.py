import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="contract-decorator", # Replace with your own username
    version="2020.10.27",
    author="Claudio Corsi",
    author_email="clcorsi@yahoo.com",
    description="A simple decorator used for parameter checking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccorsi/contract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5', # This might work for earlier version of python 3 but that has not been tested
)