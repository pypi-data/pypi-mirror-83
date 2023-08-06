import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daboi", # Replace with your own username
    version="0.0.5",
    author="Marcel Szimonisz",
    author_email="marcel.simik@gmail.com",
    description="Selenium instagram automation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msgent/daboi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
    install_requires=["selenium>=3.141.0"],
)
