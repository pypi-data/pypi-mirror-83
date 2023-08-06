from setuptools import setup, find_packages
from trejas_enlitic import version

setup(
    name="trejas_enlitic",
    version=version,
    author="Traey Hatch",
    author_email="traeyhatch@gmail.com",
    description="Funcitons to report on logs.",
    packages=find_packages(),
    entry_points={"console_scripts": ["enlitic_cli = trejas_enlitic.cli:cli"]},
    install_requires=[
        "click==7.1.2",
        "colorlog==4.2.1",
        "pandas==1.1.3",
        "tabulate==0.8.7",
    ],
    include_package_data=True,
)
