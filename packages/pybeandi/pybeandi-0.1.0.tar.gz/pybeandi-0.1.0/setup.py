import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements/base.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pybeandi",
    version="0.1.0",
    author="Aleksander Bespalov",
    author_email="discrimy.off@gmail.com",
    description="Python Dependency Injection library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Discrimy/pydi",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
