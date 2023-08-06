

from setuptools import find_packages, setup




setup(
    name="imghst",
    version="0.0.1",
    author="Mustafa Mohamed",
    author_email="ms7mohamed@gmail.com",
    description="A simple and fast image hoster for applications like ShareX.",
    long_description="A simple and fast image hoster for applications like ShareX.",
    long_description_content_type="text/markdown",
    url="https://github.com/ms7m/imghst",
    python_requires=">=3.6.0",
    packages=find_packages(
        exclude=["testing", "*.testing", "*.testing.*", "testing.*"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "imghst = imghst.entry:cli_app"
        ]
    },
    include_package_data=True,
    install_requires=open("./requirements.txt", 'r').readlines())
