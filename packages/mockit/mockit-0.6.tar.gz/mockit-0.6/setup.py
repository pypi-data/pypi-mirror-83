from distutils.core import setup
import os


def read(fname):
    with open(fname, "r") as f:
        return f.read()


long_description = read("README.md")

setup(
    name="mockit",
    description="Easy REST API mocking tool.",
    long_description="<h3>Documentation and examples are available on package's github repository.</h3>",
    long_description_content_type="text/markdown",
    packages=["mockit"],
    version="0.6",
    license="MIT",
    author="Victor Vasiliev",
    author_email="victorvasil93@gmail.com",
    url="https://github.com/victorvasil93/mockit",
    keywords=["MOCK", "SERVER", "REST", "API", "TESTS"],
    install_requires=["Flask", "pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
)
