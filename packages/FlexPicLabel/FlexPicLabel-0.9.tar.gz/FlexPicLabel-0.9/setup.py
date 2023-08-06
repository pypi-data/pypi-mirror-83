import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FlexPicLabel",
    version="0.9",
    author="Stephan Sokolow (deitarion/SSokolow), poshl9k",
    author_email="poshl9k@gmail.com",
    description="Flexible Lablel to put pictures in, for PYQT5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)