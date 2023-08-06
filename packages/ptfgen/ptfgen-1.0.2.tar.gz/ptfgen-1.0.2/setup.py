from setuptools import setup
from ptfgen import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ptfgen',
    version=__version__,
    author="Pham Xuan Tien",
    author_email="tienpx.xxx@gmail.com",
    description="A code generator for Flutter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tienpx-x/PTfGen",
    license='MIT',
    packages=['ptfgen', 'ptfgen_templates'],
    entry_points={
        'console_scripts': [
            'ptfgen = ptfgen.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    install_requires=['Jinja2>=2.10', 'arghandler>=1.2'],
    include_package_data=True
)
