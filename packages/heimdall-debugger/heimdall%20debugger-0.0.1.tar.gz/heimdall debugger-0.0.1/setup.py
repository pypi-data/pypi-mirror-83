import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="heimdall debugger", # Replace with your own username
    version="0.0.1",
    author="Matthew Proudman",
    author_email="proudmandandc@gmail.com",
    description="A small example package",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/MechaCoder/heimdall",
    packages=setuptools.find_packages(),
    install_requires=['rich'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
