from typing import List, Optional

from cognite.client import CogniteClient
from cognite.client.data_classes.assets import Asset

from cognite.well_model.client.data_classes.survey import Survey
from cognite.well_model.client.utils.sequences import list_sequences_asset


class Wellbore:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.parent_id = None
        self.__cdf_client = None
        self.__trajectory = None

    @property
    def trajectory(self) -> Optional[Survey]:
        if self.__trajectory is None:
            surveys = list_sequences_asset(self.__cdf_client, self.id, "Survey", {"Phase": "Actual"})
            def_surveys = list_sequences_asset(self.__cdf_client, self.id, "DefinitiveSurvey", {"Phase": "Actual"})
            trajectories = list_sequences_asset(self.__cdf_client, self.id, "Trajectory", {"Phase": "Actual"})
            actual = surveys + def_surveys + trajectories
            if len(actual) != 0:
                self.__trajectory = Survey.create_from_sequence(actual[0])
        return self.__trajectory

    def list_surveys(self, actual: bool = False) -> List[Survey]:
        actual_filter = {"Phase": "Actual"} if actual else {}
        surveys = list_sequences_asset(self.__cdf_client, self.id, "Survey", actual_filter)
        def_surveys = list_sequences_asset(self.__cdf_client, self.id, "DefinitiveSurvey", actual_filter)
        trajectories = list_sequences_asset(self.__cdf_client, self.id, "Trajectory", actual_filter)
        return [Survey.create_from_sequence(trajectory) for trajectory in surveys + def_surveys + trajectories]

    def get_survey_data(
        self, min_depth: float = 0.0, max_depth: Optional[float] = None, as_dataframe: bool = False
    ) -> List[List[dict]]:
        # This method only works if the data has been ingested to store the surveys in rows
        # corresponding to the depth in cms
        all_surveys = self.list_surveys()
        return [
            survey.get_data(min_depth=min_depth, max_depth=max_depth, as_dataframe=as_dataframe)
            for survey in all_surveys
        ]

    @staticmethod
    def create_from_asset(asset: Asset, cdf_client: CogniteClient):
        if asset.name is None:
            raise ValueError("Asset is missing the attribute: name")
        elif asset.id is None:
            raise ValueError("Asset is missing the attribute: id")

        wb = Wellbore(asset.name)
        wb.id = asset.id
        wb.parent_id = asset.parent_id
        wb.__cdf_client = cdf_client
        return wb
