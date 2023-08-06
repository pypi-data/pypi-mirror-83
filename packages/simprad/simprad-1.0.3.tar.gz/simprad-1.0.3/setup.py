import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simprad",
    version="1.0.3",
    author="garlicOS®",
    author_email="sisdfk@gmail.com",
    description="Simplify radicals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/the-garlic-os/simprad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
