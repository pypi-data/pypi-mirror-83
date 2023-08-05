import setuptools

setuptools.setup(
    name='lazy_computing',
    version='0.1',
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="Set of functional and lazy programming tools",
    setup_requires=['setuptools-markdown'],
    long_description_content_type="text/markdown",
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/lazy_computing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
