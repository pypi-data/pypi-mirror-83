from setuptools import setup,find_packages

setup(
    name="amantadine",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["cssutils"],
    url="https://github.com/isclub/amantadine",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    license="MIT License",
    long_description_content_type="text/markdown",
    description="Amantadine is a framework for rendering HTML on the server",
)
