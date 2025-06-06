from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="projectdump",
    version="1.0.1",
    author="Henry Vo",
    author_email="levuthanhtung11@gmail.com",
    description="A CLI tool to aggregate and dump project source code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoangneeee/projectdump",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "projectdump=projectdump.cli:main",
        ],
    },
    install_requires=[
        # Add any external dependencies here if needed
    ],
)