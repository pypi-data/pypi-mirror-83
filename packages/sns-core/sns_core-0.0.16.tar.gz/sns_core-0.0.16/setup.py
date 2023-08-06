import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sns_core",
    version="0.0.16",
    author="Soter Company",
    author_email="soter.business@gmail.com",
    description="SNS-core provides all the core functions to communicate using the SNS protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/sns-core/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='tests.test_suite',
    install_requires=[
        
    ],
)