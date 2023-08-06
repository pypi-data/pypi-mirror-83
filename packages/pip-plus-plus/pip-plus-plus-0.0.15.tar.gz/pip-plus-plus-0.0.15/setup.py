import setuptools

try:
    with open("pipplusplus/README.md", "r") as fh:
        long_description = fh.read()
except Exception:
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="pip-plus-plus",
    version="0.0.15",
    author="Idan Cohen",
    include_package_data=True,
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