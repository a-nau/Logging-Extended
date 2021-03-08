import setuptools

setuptools.setup(
    name="logging-extended",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=['GitPython>=2.1.11'],
    package_data={"logging_extended": ["logging_config.ini", "logging_config_console.ini"]},
    author='Alexander Naumann',
    author_email='alexander@naumail.de',
)
