from setuptools import find_packages, setup

setup(
    name="dbt_ragster",
    packages=find_packages(exclude=["dbt_ragster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
