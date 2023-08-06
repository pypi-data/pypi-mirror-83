import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a8a8a8a8a8a8a8a8a8a8a8a8a8a8a8",
    version="1.0.4",
    author="JoeAmedeo",
    author_email="joseph.p.amedeo@gmail.com",
    description="Listen to your favourite audiobook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoeAmedeo/audiobook",
    keywords="audiobook",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.4",
)
