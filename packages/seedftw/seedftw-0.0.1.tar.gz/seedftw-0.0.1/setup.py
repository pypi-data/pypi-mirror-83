import setuptools

setuptools.setup(
    name="seedftw",
    version="0.0.1",
    author="PVF",
    author_email="pvf@dtime.ai",
    description="Simple Energy & Environment Data From The World (aka. seedftw) - A small example package for acquiring open energy and ennvironment data",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Pierre_VF/seedftw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    requires = [
        "dash",
        "datetime",
        "functools",
        "json",
        "numpy",
        "os",
        "pandas",
        "plotly",
        "setuptools",
        "urllib"],
    install_requires = [
        "dash",
        "datetime",
        "numpy",
        "pandas",
        "plotly"]
)

# More details on how to set this up: https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html