import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="lance",
        version="0.1.1",
        author="Supratim Samanta",
        author_email="tech.supratim.samanta@gmail.com",
        description="A helper package to generate code from declarative json",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/susamn/lance",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
