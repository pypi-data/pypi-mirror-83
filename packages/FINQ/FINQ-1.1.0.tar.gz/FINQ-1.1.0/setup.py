import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FINQ", # Replace with your own username
    version="1.1.0",
    author="FacelessLord",
    author_email="skyres21@gmail.com",
    description="Lightweight conveyor data processing python framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FacelessLord/FINQ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)