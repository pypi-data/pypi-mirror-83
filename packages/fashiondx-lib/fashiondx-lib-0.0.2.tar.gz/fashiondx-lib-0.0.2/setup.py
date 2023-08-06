import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fashiondx-lib",
    version="0.0.2",
    author="Rakshit Sharma",
    author_email="rakshit@fashiondx.co",
    description="fdx lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['fdx_utils','method_tree_parser','datasources','datasources.datasource'],
    url="https://github.com/FashionDx/fdx-lib",
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'pymongo',
        'elasticsearch'
    ],
    python_requires='>=3.6',
)
