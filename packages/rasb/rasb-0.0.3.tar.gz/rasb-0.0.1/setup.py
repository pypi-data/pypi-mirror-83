import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasb", # Replace with your own username
    version="0.0.1",
    author="M_ultii",
    author_email="multiidev@gmail.com",
    description="RASB Bot API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstroMulti/RASB-Python-API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)