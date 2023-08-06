import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="arcgisUtils",
    version="0.0.1",
    description="Functions to interact with the api in arcgis online.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vizzTools/arcgisUtils",
    author="Vizzuality",
    author_email="greta.carrete@vizzuality.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=['arcgisUtils'],
    install_requires=['requests>=2.2.0', 'arcgis>=1.8.2'],
    entry_points={
        "console_scripts": [
            "vizzpython=arcgisUtils.__main__:main",
        ]
    },
)
