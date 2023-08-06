import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Generator-Random",
    version="0.0.2",
    author="Abhijeet Srivastav,  Founder Techneophyte",
    author_email="abhijeetsrivastav292@gmail.com",
    description="Generator is an All In One python package to generate random names,MAC,IP,email, password,pin and integer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


