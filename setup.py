import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phdler",
    version="0.0.13",
    author="Mario Semeš",
    author_email="phdler@mariosem.es",
    description="Downloading made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['phdler=phdler:main'],
    },
    python_requires='>=3.5',
)