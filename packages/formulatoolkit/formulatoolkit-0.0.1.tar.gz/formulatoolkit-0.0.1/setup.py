import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="formulatoolkit", # Replace with your own username
    version="0.0.1",
    author="Alessio Palma",
    author_email="ozw1z5rd@gmail.com",
    description="Formula toolkit ( pure python code )",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ozw1z5rd/py-expression-eval.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)