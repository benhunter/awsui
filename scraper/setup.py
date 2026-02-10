from setuptools import setup, find_packages

setup(
    name="awsui-scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.34.0",
        "pyyaml>=6.0.1",
        "python-dateutil>=2.8.2",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "awsui-scraper=src.cli:main",
        ],
    },
)
