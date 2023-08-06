import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid19_jhu_data",
    version="0.0.2",
    author="Kuo, Yao-Jen",
    author_email="yaojenkuo@datainpoint.com",
    description="We use pandas to import data from https://github.com/CSSEGISandData/COVID-19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pandas>=1'
    ]
)