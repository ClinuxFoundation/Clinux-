from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clinux",
    version="1.0.0",
    author="CLINUX Team",
    description="CLI tool para gerenciar ambientes Linux com QEMU e PRoot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clinux/clinux",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=8.0",
        "rich>=10.0",
        "pyyaml>=5.4",
        "requests>=2.25",
        "psutil>=5.8",
    ],
    entry_points={
        "console_scripts": [
            "clinux=clinux.cli:main",
        ],
    },
)