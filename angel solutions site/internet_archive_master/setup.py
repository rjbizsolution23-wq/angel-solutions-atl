"""
Internet Archive Ultimate Master System
Installation Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="internet-archive-master",
    version="1.0.0",
    author="RJ PROMETHEUS APEX",
    author_email="support@rickjeffersonsolutions.com",
    description="Complete Internet Archive API integration system with AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rjbizsolution23-wq/internet-archive-master",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.32.0",
        "click>=8.1.0",
        "rich>=13.7.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
            "mypy>=1.10.0",
        ],
        "async": [
            "aiohttp>=3.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ia=cli.ia_cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
