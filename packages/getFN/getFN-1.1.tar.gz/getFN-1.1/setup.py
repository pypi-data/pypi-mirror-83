import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getFN", # Replace with your own username
    version="1.1",
    author="hunter g",
    author_email="redissuslolol@gmail.com",
    description="Lightweight module for get filenames & file exts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.beyonce.com/',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
