import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nuvpy", 
    version="1.0.1",
    author="Software Logistics, LLC",
    author_email="kevinw@software-logistics.com",
    description="Python libraries for access of data generated from IoT devices captured with NuvIoT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lagovista/nuvpy",
    packages=setuptools.find_packages(),
    keywords=['NuvIoT','IoT','Devices','Machine Learning'],
    download_url="https://github.com/lagovista/nuvpy/archive/v_1.0.1.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)