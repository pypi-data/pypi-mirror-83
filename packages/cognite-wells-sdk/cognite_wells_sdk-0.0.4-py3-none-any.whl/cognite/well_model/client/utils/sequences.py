from typing import Dict, List, Optional

from cognite.client import CogniteClient
from cognite.client.data_classes.sequences import Sequence


def list_sequence_type(client: CogniteClient, sequence_type: str) -> List[Sequence]:
    return client.sequences.list(metadata={"type": sequence_type}, limit=None)


def list_sequences_asset_subtree(client: CogniteClient, asset_id: int, sequence_type: str) -> List[Sequence]:
    return client.sequences.list(asset_subtree_ids=[asset_id], metadata={"type": sequence_type}, limit=None)


def list_sequences_asset(
    client: CogniteClient, asset_id: int, sequence_type: str, metadata_filter: Optional[Dict[str, str]] = None
) -> List[Sequence]:
    md_filter = {} if metadata_filter is None else metadata_filter
    return client.sequences.list(asset_ids=[asset_id], metadata={"type": sequence_type, **md_filter}, limit=None)
