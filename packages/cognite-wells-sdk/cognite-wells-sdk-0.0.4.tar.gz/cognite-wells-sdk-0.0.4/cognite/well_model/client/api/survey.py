from typing import List, Optional, Union

from cognite.client import CogniteClient

from cognite.well_model.client.data_classes.survey import Survey
from cognite.well_model.client.data_classes.wellbores import Wellbore
from cognite.well_model.client.data_classes.wells import Well
from cognite.well_model.client.utils.sequences import list_sequence_type, list_sequences_asset_subtree


class SurveyAPI:
    def __init__(self, client: CogniteClient):
        self.cdf_client = client

    def list_all(self, well: Optional[Union[Well, Wellbore]] = None) -> List[Survey]:
        if well is None:
            surveys = list_sequence_type(self.cdf_client, "Survey")
            definitive_surveys = list_sequence_type(self.cdf_client, "DefinitiveSurvey")
            trajectories = list_sequence_type(self.cdf_client, "Trajectory")
        else:
            surveys = list_sequences_asset_subtree(self.cdf_client, well.id, "Survey")
            definitive_surveys = list_sequences_asset_subtree(self.cdf_client, well.id, "DefinitiveSurvey")
            trajectories = list_sequences_asset_subtree(self.cdf_client, well.id, "Trajectory")
        return [Survey.create_from_sequence(survey) for survey in surveys + definitive_surveys + trajectories]
