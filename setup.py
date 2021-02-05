import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plm", # Replace with your own username
    version="0.0.1",
    author="Xing Han Lu",
    author_email="github@xinghanlu.com",
    description="Helps you manage python libraries and environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xhlulu/plm",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'plm=plm:main'
        ]
    }
)