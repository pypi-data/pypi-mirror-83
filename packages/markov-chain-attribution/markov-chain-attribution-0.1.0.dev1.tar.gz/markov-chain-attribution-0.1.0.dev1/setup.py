from setuptools import find_packages
from setuptools import setup

import markov_chain_attribution as mca

with open("README.md", encoding='utf8') as readme:
    long_description = readme.read()

with open("requirements.txt", encoding='utf8') as requirements_txt:
    install_requirements = requirements_txt.readlines()

download_url = f"https://github.com/ritikjain51/markov-chain-attribution/releases/tag/v{mca.__version__}"

setup(
    name="markov-chain-attribution",
    version=mca.__version__,
    description='Digital Market Attribution',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ritik Jain',
    url='https://github.com/ritikjain51/markov-chain-attribution',
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    download_url=download_url,
    keywords="markov-chain-attribution markov attribution monte carlo",
    install_requires=install_requirements,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Office/Business :: Financial",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    options={"bdist_wheel": {"universal": True}},
)
