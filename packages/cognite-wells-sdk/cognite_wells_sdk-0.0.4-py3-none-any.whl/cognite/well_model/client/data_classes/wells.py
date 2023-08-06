from typing import Dict, Optional

from cognite.client.data_classes.assets import Asset

from cognite.well_model.client.data_classes.const import (
    COUNTRY,
    DATUM,
    DATUM_ELEV,
    DATUM_UNIT,
    LOC_CRS,
    LOC_X,
    LOC_Y,
    PLATFORM,
    SOURCE_MD_PREFIX,
)
from cognite.well_model.client.utils.assets import find_source_asset_ids


class WellLocation:
    def __init__(self, loc_x: str, loc_y: str, unit: str = "m", crs: str = "epsg:4326"):
        self.x = loc_x
        self.y = loc_y
        self.unit = unit
        self.crs = crs


class WellDatum:
    def __init__(self, name: str, elevation: float, unit: str):
        self.name = name
        self.elevation = elevation
        self.unit = unit


class Well:
    def __init__(
        self,
        name: str,
        external_id: str,
        loc_x: str,
        loc_y: str,
        loc_crs: str,
        loc_unit: str = "m",
        datum_name: str = "MSL",
        datum_elevation: float = 0.0,
        datum_unit: str = "m",
        country: Optional[str] = None,
        platform: Optional[str] = None,
        source_metadata: Dict[str, int] = {},
    ):
        self.name = name
        self.cdf_id = None
        self.external_id = external_id
        self.location = WellLocation(loc_x=loc_x, loc_y=loc_y, unit=loc_unit, crs=loc_crs)
        self.datum = WellDatum(name=datum_name, elevation=datum_elevation, unit=datum_unit)
        self.country = country
        self.platform = platform
        self.source_metadata = source_metadata

    @staticmethod
    def from_asset(asset: Asset):
        if asset.name is None:
            raise ValueError("Asset is missing the attribute: name")
        for val in [LOC_X, LOC_Y, LOC_CRS]:
            if val not in asset.metadata.keys():
                raise ValueError(f"Asset is missing the metadata field: {val}")
            elif asset.metadata[val] is None:
                raise ValueError(f"Asset is missing the metadata value: {val}")
        well = Well(
            name=asset.name,
            external_id=asset.external_id,
            loc_x=asset.metadata[LOC_X],
            loc_y=asset.metadata[LOC_Y],
            loc_crs=asset.metadata[LOC_CRS],
        )
        if asset.id:
            well.cdf_id = asset.id
        if asset.metadata.get(DATUM_ELEV) is not None:
            well.datum = WellDatum(asset.metadata[DATUM], float(asset.metadata[DATUM_ELEV]), asset.metadata[DATUM_UNIT])
        well.source_metadata = find_source_asset_ids(asset)
        return well

    def to_asset(self, dataset_id: Optional[int] = None) -> Asset:
        """
        reference implementation for wells ingested by ingestion.WellHeaderIngestor
        """
        asset = Asset()
        asset.name = self.name
        asset.external_id = self.external_id
        # TODO if we keep a cdf client as an internal attribute of the well, we can find this using fixed external id
        if dataset_id:
            asset.data_set_id = dataset_id
        asset.metadata = {
            LOC_X: self.location.x,
            LOC_Y: self.location.y,
            LOC_CRS: self.location.crs,
        }
        if self.country:
            asset.metadata[COUNTRY] = self.country
        if self.platform:
            asset.metadata[PLATFORM] = self.platform
        if self.datum:
            asset.metadata[DATUM] = self.datum.name
            asset.metadata[DATUM_ELEV] = str(self.datum.elevation)
            asset.metadata[DATUM_UNIT] = self.datum.unit
        for source in self.source_metadata.keys():
            asset.metadata[f"{SOURCE_MD_PREFIX}{source}"] = str(self.source_metadata[source])

        return asset
