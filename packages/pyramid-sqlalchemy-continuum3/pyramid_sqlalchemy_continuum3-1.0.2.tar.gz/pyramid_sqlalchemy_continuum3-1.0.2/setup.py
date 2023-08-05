import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyramid_sqlalchemy_continuum3",  # Replace with your own username
    version="1.0.2",
    author="Lehan Coetzee (Jordi Fernández <jfernandez@bioiberica.com>)",
    author_email="haaslewer2@gmail.com",
    description="PyramidPlugin offers way of integrating Pyramid framework with SQLAlchemy-Continuum.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HAASLEWER/pyramid_sqlalchemy_continuum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
