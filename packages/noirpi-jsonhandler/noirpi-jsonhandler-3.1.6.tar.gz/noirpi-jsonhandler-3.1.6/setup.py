import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noirpi-jsonhandler",  # Replace with your own username
    version="3.1.6",
    author="NoirPi",
    author_email="noirpi@noircoding.de",
    description="A small json Filehandler",
    long_description="A small json Filehandler which i use in my own projects to simplify "
                     "messing arround with json files.",
    long_description_content_type="text/markdown",
    url="https://github.com/noirpi/json-filehandler",
    packages=['jsonhandler'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ],
    python_requires='>=3.6',
    zip_safe=False
)
