import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jikipedia",
    version="0.5.2-DEV",
    author="HanTools",
    author_email="hantools@foxmail.com",
    description="小鸡词典API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daizihan233/jikipedia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests']
)
