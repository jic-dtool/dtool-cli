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
    install_requires=[
        "click",
        "click-plugins",
        "dtoolcore>=2",
    ],
    entry_points={
        'console_scripts': ['dtool=dtool_cli.cli:dtool'],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
