import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rs_tools",
    version="0.2",
    author="Darel",
    author_email="darel142857@gmail.com",
    description="Recommender systems related tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darel13712/rs_tools",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'numpy', 'implicit', 'scipy', 'sklearn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
