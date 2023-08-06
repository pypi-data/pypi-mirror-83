from typing import Dict, List, Optional

from cognite.client.data_classes.sequences import Sequence


class Survey:
    def __init__(
        self,
        name: str,
        asset_id: int,
        external_id: str,
        cdf_id: Optional[int] = None,
        description: str = "",
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.id = cdf_id
        self.name = name
        self.description = description
        self.asset_id = asset_id
        self.external_id = external_id
        self.metadata = metadata
        self.__sequence = None

    @property
    def seq(self):
        return self.__sequence

    def get_data(
        self, min_depth: float = 0.0, max_depth: Optional[float] = None, as_dataframe: bool = False
    ) -> List[dict]:
        if self.__sequence is not None:
            end_value = int(100 * max_depth) if max_depth is not None else max_depth
            rows = self.__sequence.rows(start=int(100 * min_depth), end=end_value)
            if as_dataframe:
                rows = rows.to_pandas()
            return rows
        return []

    @staticmethod
    def create_from_sequence(sequence: Sequence):
        if sequence.name is None:
            raise ValueError("Sequence is missing the attribute: name")
        elif sequence.id is None:
            raise ValueError("Sequence is missing the attribute: id")
        elif sequence.asset_id is None:
            raise ValueError("Sequence is missing the attribute: asset_id")
        elif sequence.external_id is None:
            raise ValueError("Sequence is missing the attribute: external_id")

        seq = Survey(
            sequence.name, sequence.asset_id, sequence.external_id, sequence.id, sequence.description, sequence.metadata
        )
        seq.__sequence = sequence
        return seq
