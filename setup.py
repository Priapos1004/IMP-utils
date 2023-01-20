from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="IMP_utils_py",
    version="0.0.1",
    description="stuff to make your IMP life easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={},
    scripts=[],
    install_requires=[
        "pandas",
        "numpy",
        #"ipykernel",
        "gin-config",
        "absl-py",
    ],
    extras_require={
        "test": ["pytest", "pylint!=2.5.0", "isort", "refurb"],
    },
    author="Samuel Brinkmann",
    license="MIT",
    tests_require=["pytest==4.4.1"],
    setup_requires=["pytest-runner"],
)
