import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='apicli',
    version='0.0.4',
    packages=setuptools.find_packages(),
    description='allow using a common code-base to create a REST API and a CLI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sylvan Le Deunff',
    author_email='sledeunf@gmail.com',
    url='https://github.com/sylvan-le-deunff/apicli',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
