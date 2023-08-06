import logging
from typing import List, Optional

from cognite.client.data_classes.assets import Asset, AssetFilter
from cognite.geospatial.types import Geometry, SpatialRelationship

from cognite.well_model.client.data_classes.wells import Well

logger = logging.getLogger("cognite.well_model.client.api.wells")


class WellAPI:
    def __init__(self, cdf_client, geospatial):
        self.cdf_client = cdf_client
        self.geo_client = geospatial

    def get_datum(self, well_id: int) -> Optional[Asset]:
        data = self.cdf_client.assets.list(parent_ids=[well_id], metadata={"type": "Datum"})
        if len(data) > 0:
            return data[0]
        return None

    def get_by_id(self, well_id: int) -> Optional[Well]:
        asset = self.cdf_client.assets.retrieve(id=well_id)
        if asset is not None:
            return Well.from_asset(asset)
        logger.info(f"Well with the id: {well_id} does not exist.")
        return None

    def get_by_ext_id(self, ext_id: str) -> Optional[Well]:
        assets = self.cdf_client.assets.list(ext_id=ext_id, metadata={"type": "Well"})
        if len(assets) > 0:
            return Well.from_asset(assets[0])
        logger.info(f"Well with the external id: {ext_id} cannot be found.")
        return None

    def get_by_name(self, name: str) -> List[Well]:
        assets = self.cdf_client.assets.list(name=name, metadata={"type": "Well"})
        return [Well.from_asset(asset) for asset in assets]

    def geo_search(
        self,
        polygon: str,
        crs: str,
        limit: int = 10,
        layer_name: str = "point",
        timeout: int = 10,
    ) -> List[Well]:
        wells: List[Well] = []
        i = 0
        while len(wells) < limit and i < timeout:
            points = self.geo_client.find_spatial(
                layer=layer_name,
                spatial_relationship=SpatialRelationship.within,
                geometry=Geometry(wkt=polygon, crs=crs),
                limit=1000,
                offset=i * 1000,
            )
            points = [point for point in points if point.asset_ids != []]
            for point in points:
                try:
                    if len(wells) < limit:
                        for asset_id in point.asset_ids:
                            wells.append(self.get_by_id(well_id=asset_id))
                except ValueError as e:
                    logging.error(str(e) + f" for point {point.id}")
            i += 1
        return wells

    def list(self, name_prefix: str):
        asset_filter = AssetFilter(metadata={"type": "Well"})
        well_assets = [
            well
            for well in self.cdf_client.assets.search(name=name_prefix, filter=asset_filter)
            if well.name.startswith(name_prefix)
        ]
        return [Well.from_asset(asset) for asset in well_assets]

    def create(self, well: Well):
        pass
