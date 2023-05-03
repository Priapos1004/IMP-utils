from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="IMP_utils_py",
    version="0.0.2-v2",
    description="stuff to make your IMP life easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
    packages=find_packages(),
    package_data={},
    scripts=[],
    install_requires=[
        "pandas",
        "numpy",
        "gin-config",
        "absl-py",
        "keyboard; platform_system=='Windows'", # only on Windows needed
        "matplotlib",
        "scipy",
        "kafe2",
        "iminuit", # better performance with c++ library for kafe2
        "openpyxl", # needed for pandas read_excel
    ],
    extras_require={
        "test": ["pytest", "pylint!=2.5.0", "isort", "refurb"],
        "notebook": ["ipykernel"],
    },
    author="Samuel Brinkmann",
    license="MIT",
    tests_require=["pytest==4.4.1"],
    setup_requires=["pytest-runner"],
)
