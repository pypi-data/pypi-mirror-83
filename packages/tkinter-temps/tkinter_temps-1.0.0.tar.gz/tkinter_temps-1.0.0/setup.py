import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkinter_temps",
    version="1.0.0",
    author="hunterg",
    author_email="redissuslolol@gmail.com",
    description="A module for ease of making GUI's in Tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.beyonce.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'docifyPLUS',
        'lambdaChaining'
    ]
)