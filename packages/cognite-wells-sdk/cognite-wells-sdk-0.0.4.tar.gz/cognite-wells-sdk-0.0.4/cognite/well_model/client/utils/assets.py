from typing import Dict

from cognite.client.data_classes import Asset

from cognite.well_model.client.data_classes.const import SOURCE_MD_PREFIX


def find_source_asset_ids(asset: Asset) -> Dict[str, int]:
    sources = {}
    asset_md = asset.metadata
    for attr in asset_md.keys():
        if attr.startswith(SOURCE_MD_PREFIX):
            source_name = attr.split(SOURCE_MD_PREFIX)[-1]
            sources[source_name] = int(asset_md.get(attr))
    return sources
