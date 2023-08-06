from setuptools import setup, find_packages

setup(
    name="sentence_spliter",
    version="1.0.5",
    author="bohuai jiang",
    author_email="highjump000@hotmail.com",
    description="This is a sentence cutting tool that supports long sentence segmentation and short sentence merging.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    # package_dir={"":"sentence_spliter"},
    packages=['sentence_spliter'],

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    REQUIRES_PYTHON='>=3.6.0',
    install_requires=['attrd>=2.0.1']
)
