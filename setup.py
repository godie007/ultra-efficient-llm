"""
Setup para UltraEfficientLLM
"""

from setuptools import setup, find_packages
import os

# Leer README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Leer requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ultra-efficient-llm",
    version="1.0.0",
    author="UltraEfficientLLM Team",
    author_email="team@ultra-efficient-llm.com",
    description="Modelo de lenguaje ultra-eficiente basado en patrones selectivos",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ultra-efficient-llm/ultra-efficient-llm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ultra-efficient-llm=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
    keywords="machine learning, natural language processing, efficient, patterns, llm",
    project_urls={
        "Bug Reports": "https://github.com/ultra-efficient-llm/ultra-efficient-llm/issues",
        "Source": "https://github.com/ultra-efficient-llm/ultra-efficient-llm",
        "Documentation": "https://ultra-efficient-llm.readthedocs.io/",
    },
) 