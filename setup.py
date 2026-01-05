"""
Kakuro Puzzle Book Generator - Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="kakuro-generator",
    version="0.1.0",
    description="Automated Kakuro puzzle book generator for Amazon KDP publishing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vikas Rijsinghani",
    author_email="vikasrij@gmail.com",
    url="https://github.com/vrijsinghani/kakuro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
        "graphics": [
            "cairosvg>=2.7.0",
            "pycairo>=1.25.0",
        ],
        "analytics": [
            "pandas>=2.1.0",
            "openpyxl>=3.1.0",
            "requests>=2.31.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kakuro-generate=scripts.batch_generation.generate_puzzles:main",
            "kakuro-build=scripts.batch_generation.create_interior:main",
            "kakuro-validate=scripts.quality_control.validate_book:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Printing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="kakuro puzzle generator kdp amazon publishing pdf reportlab",
    project_urls={
        "Documentation": "https://github.com/vrijsinghani/kakuro/docs",
        "Source": "https://github.com/vrijsinghani/kakuro",
        "Tracker": "https://github.com/vrijsinghani/kakuro/issues",
    },
)

