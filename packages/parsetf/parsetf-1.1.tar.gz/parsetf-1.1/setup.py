import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="parsetf",
    version="1.1",
    author="web",
    author_email="willweb@126.com",
    description="parse terraform template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        "parsetf": [
            "*.py",
            "*.so",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    install_requires=[],
    python_requires='>=3.6',
)
