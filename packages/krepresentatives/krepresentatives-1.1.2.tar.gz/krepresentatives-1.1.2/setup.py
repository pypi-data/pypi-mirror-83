import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="krepresentatives", 
    version="1.1.2",
    author="Toan Nguyen Mau and Van-Nam Huynh",
    author_email="nmtoan91@jaist.ac.jp",
    description="A package for k-Representatives and LSH-k-Representatives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)