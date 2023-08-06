from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_requires():
    with open("requirements.txt","r") as requirements:
        return list(requirements.readlines()) 

setup(
    name="handlers-lauto",
    version="1.0.4",
    author="L'auto Cargo Transportes Rodoviário S/A",
    author_email="suporte.lautotech@gmail.com",
    description="Pacote para gerenciamento de logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/nexfrete/handlers/src/master/",
    license="MIT License",
    packages=find_packages(),
    install_requires=get_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
