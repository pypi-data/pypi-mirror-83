from typing import Dict, List

from setuptools import find_packages, setup

REQUIREMENTS: Dict[str, List[str]] = {
    "install": [],
    "develop": [],
    "test": [],
}

with open("README.md", "r", encoding="utf-8") as readme:
    README_CONTENTS = readme.read()

setup(
    name="fixings",
    version="0.0.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="Bulat Bochkariov",
    author_email="fixings@bulat.bochkariov.com",
    description="Composable test-data fixtures for SQLAlchemy apps",
    long_description=README_CONTENTS,
    long_description_content_type="text/markdown",
    url="https://github.com/bulatb/fixings",
    project_urls={
        "Source": "https://github.com/bulatb/fixings",
        "Issues": "https://github.com/bulatb/fixings/issues",
    },
    install_requires=REQUIREMENTS["install"],
    extras_require={
        "develop": set(REQUIREMENTS["develop"] + REQUIREMENTS["test"]),
        "test": REQUIREMENTS["test"],
    },
    python_requires=">=3.6",
    keywords="data fixtures testing sqlalchemy",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
    ],
)
