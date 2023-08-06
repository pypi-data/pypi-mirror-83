import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cameralyze-toolkit",
    version="0.0.2",
    author="Cameralyze",
    author_email="info@cameralyze.com",
    description="Cameralyze - Python Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdullahkulcu/Camper-Logger-Exception",
    packages=setuptools.find_packages(),
    install_requires=[
        "psycopg2-binary==2.8.6",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)