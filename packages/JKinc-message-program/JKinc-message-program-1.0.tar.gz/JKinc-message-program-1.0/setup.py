import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JKinc-message-program", # Replace with your own username
    version="1.0",
    author="JKinc",
    author_email="G.T.H.T.I.A.T.A@gmail.com",
    description="Encrypted Messaging Program for LAN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)