from typing import List

from cognite.client import CogniteClient

from cognite.well_model.client.data_classes.wellbores import Wellbore


class WellboreAPI:
    def __init__(self, cdf_client: CogniteClient):
        self.cdf_client = cdf_client

    def list_all(self) -> List[Wellbore]:
        return [
            Wellbore.create_from_asset(asset, self.cdf_client)
            for asset in self.cdf_client.assets.list(metadata={"type": "Wellbore"}, limit=None)
        ]

    def list_children(self, parent_id: int) -> List[Wellbore]:
        return [
            Wellbore.create_from_asset(asset, self.cdf_client)
            for asset in self.cdf_client.assets.list(metadata={"type": "Wellbore"}, parent_ids=[parent_id], limit=None)
        ]

    def list_all_in_well(self, well_id: int) -> List[Wellbore]:
        well = self.cdf_client.assets.retrieve(id=well_id)
        if well is None:
            raise ValueError(f"Asset with id: {well_id} does not exist")
        if well.metadata.get("type") == "Well":
            return [
                Wellbore.create_from_asset(asset, self.cdf_client)
                for asset in self.cdf_client.assets.list(
                    metadata={"type": "Wellbore"}, asset_subtree_ids=[well_id], limit=None
                )
            ]
        raise ValueError(f"Asset with id: {well_id} is not a well")
