import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eaglet",  # Replace with your own username
    version="0.0.2",
    author="Eminjan Turamat",
    author_email="yiminjiang@ainnovation.com",
    description="Time Series Forecasting Toolkits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mtax/eaglet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
