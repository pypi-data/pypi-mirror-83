import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MyPipeline4Python",
    version="0.0.1",
    author="Tiberio Falsiroli, Lorenzo di Tria, Giovanni Donato Gallo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)
