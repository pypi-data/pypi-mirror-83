import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multitrim",
    version="1.0.1",
    author="Kenji Gerhardt",
    author_email="kenji.gerhardt@gmail.com",
    description="A readtrimming and quality control pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KGerhardt/multitrim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: iOS",
		"Operating System :: Unix"
    ],
    python_requires='>=3.6',
	entry_points={
        "console_scripts": [
            "multitrim=multitrim.multitrim:main",
        ]
    }
)