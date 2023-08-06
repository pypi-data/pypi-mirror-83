import setuptools

with open("pip-plus-plus/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip-plus-plus",
    version="0.0.5",
    author="Idan Cohen",
    author_email="idan57@gmail.com",
    description="Pip++",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idan57/pip-plus-plus",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)