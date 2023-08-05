import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GreenDeck_GsheetsTest", # Replace with your own username
    version="0.0.17",
    author="Sneh Kothari",
    author_email="snehkothari1@gmail.com",
    description="Greendeck Test to plot graph using gsheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snehkothari/GreenDeck_gsheets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
          'matplotlib',
          'pandas',
          'gsheets',
      ],
)