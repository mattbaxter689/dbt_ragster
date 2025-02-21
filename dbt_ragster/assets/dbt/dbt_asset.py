import os
from pathlib import Path
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject
from dagster import AssetExecutionContext

dbt_project_project = DbtProject(
    project_dir=Path(__file__)
    .joinpath("..", "..", "..", "..", "dbt_project")
    .resolve(),
)
dbt_project_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project_project.manifest_path)
def dbt_ragster_dbt_asset(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
