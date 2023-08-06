import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawler-api",  # Replace with your own username
    version="0.3",
    author="CooperHan",
    author_email="wy2208293418@163.com",
    description="A sample Crawler API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomersHan/AI-X-crawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",

    ],
    python_requires='>=3.6',
)
