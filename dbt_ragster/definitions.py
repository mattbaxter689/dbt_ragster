from dagster import Definitions, load_assets_from_package_module

from dbt_ragster.assets import reddit

reddit_assets = load_assets_from_package_module(reddit, group_name="reddit")

all_assets = [*reddit_assets]

defs = Definitions(
    assets=all_assets,
)
