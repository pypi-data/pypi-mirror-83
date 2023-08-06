import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tinycat",
    version="0.1",
    author="Kamil Bobrowski",
    author_email="kamil.bobrowski@gmail.com",
    description="A tiny Computer-Assisted Translation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kbobrowski/tinycat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'deep_translator'
    ],
    python_requires='>=3.6',
)