import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="financespy_cli",
    version="0.0.1",
    author="Danilo Mendonça Oliveira",
    author_email="danilomendoncaoliveira@gmail.com",
    description="The command line interface for the FinancesPy API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danilomo/FinancesPy-CLI",
    packages=setuptools.find_packages(),
    python_requires=">= 3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points = {
        'console_scripts': ['financespy=financespy_cli.main:main'],
    }
)
