from typing import Callable, Dict, Optional, Union

from cognite.client import CogniteClient
from cognite.geospatial import CogniteGeospatialClient

from cognite.well_model.client.api.survey import SurveyAPI
from cognite.well_model.client.api.wellbores import WellboreAPI
from cognite.well_model.client.api.wells import WellAPI


class WellsClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        project: Optional[str] = None,
        client_name: Optional[str] = None,
        base_url: Optional[str] = None,
        max_workers: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        token: Optional[Union[str, Callable[[], str], None]] = None,
        disable_pypi_version_check: Optional[bool] = None,
        debug: Optional[bool] = False,
    ):
        self.cdf = CogniteClient(
            api_key=api_key,
            project=project,
            client_name=client_name,
            base_url=base_url,
            max_workers=max_workers,
            headers=headers,
            timeout=timeout,
            token=token,
            disable_pypi_version_check=disable_pypi_version_check,
            debug=debug,
        )
        self.geo_client = CogniteGeospatialClient(api_key=api_key, project=project)
        self.wells = WellAPI(self.cdf, self.geo_client)
        self.wellbores = WellboreAPI(self.cdf)
        self.surveys = SurveyAPI(self.cdf)
