import setuptools

classifiers = [
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License",
    # "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: OS Independent",
    "Intended Audience :: Education",
    "Development Status :: 5 - Production/Stable",
    "Topic :: Software Development"
]

with open("README.md", "r") as fh:
    readme = fh.read()

with open ("CHANGELOG.txt") as cl:
    changeLog = cl.read()


setuptools.setup(
    name = "example-pkg-zumrudu-anka", # Replace with your own username
    version = "0.0.2",
    author = "Zümrüd-ü Anka",
    author_email = "osmandurdag@hotmail.com",
    description = "A small example package",
    long_description = f"{readme}\n\n{changeLog}",
    long_description_content_type = "text/markdown",
    url = "https://github.com/zumrudu-anka/python-upload-package-boilerplate",
    packages = setuptools.find_packages(),
    classifiers = classifiers,
    python_requires = '>=3', # "can use !=3.0.*, ~=3.3 -> not 4 but can be <3.3, 3.4, ... , 3.9>"
    install_requires = [""],
    keywords = "upload-python-package calculator"
)