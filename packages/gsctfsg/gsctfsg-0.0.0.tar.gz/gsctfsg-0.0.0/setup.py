import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsctfsg", # Replace with your own username
    author="gsctfsg",
    author_email="gabectfrepo@gmail.com",
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url='https://github.com/GSCTF/gsctfpip/archive/v1.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

