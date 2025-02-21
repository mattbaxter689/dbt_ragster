from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import DbtCliResource
from dbt_ragster.assets import reddit
from dbt_ragster.assets import dbt
from dbt_ragster.dbt_ragster.assets.dbt.dbt_asset import dbt_project_project

reddit_assets = load_assets_from_package_module(reddit, group_name="reddit")
dbt_assets = load_assets_from_package_module(dbt, group_name="dbt_assets")

all_assets = [*reddit_assets, *dbt_assets]

defs = Definitions(
    assets=all_assets,
    resources={"dbt": DbtCliResource(project_dir=dbt_project_project)},
)
