import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opustools",
    version="1.2.1",
    author="Mikko Aulamo",
    author_email="mikko.aulamo@helsinki.fi",
    description="Tools to read OPUS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Helsinki-NLP/OpusTools",
    packages=setuptools.find_packages(),
    scripts=["bin/opus_read", "bin/opus_cat", "bin/opus_get",
        "bin/opus_langid", "bin/opus_express"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
