from setuptools import setup

url = "https://github.com/jic-dtool/dtool-cli"
version = "0.7.1"
readme = open('README.rst').read()

setup(
    name="dtool-cli",
    packages=["dtool_cli"],
    version=version,
    description="Data management command line tool: dtool.",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    url=url,
    python_requires=">=3.9",
    install_requires=[
        "click",
        "click-plugins",
        "dtoolcore>=2",
    ],
    entry_points={
        'console_scripts': ['dtool=dtool_cli.cli:dtool'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
