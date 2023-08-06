from typing import Any, Dict, List, Optional

import attr

from ..models.dna_sequence_bulk_update import DnaSequenceBulkUpdate


@attr.s(auto_attribs=True)
class DnaSequencesBulkUpdate:
    """  """

    dna_sequences: Optional[List[DnaSequenceBulkUpdate]] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.dna_sequences is None:
            dna_sequences = None
        else:
            dna_sequences = []
            for dna_sequences_item_data in self.dna_sequences:
                dna_sequences_item = dna_sequences_item_data.to_dict()

                dna_sequences.append(dna_sequences_item)

        return {
            "dnaSequences": dna_sequences,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequencesBulkUpdate":
        dna_sequences = []
        for dna_sequences_item_data in d.get("dnaSequences") or []:
            dna_sequences_item = DnaSequenceBulkUpdate.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        return DnaSequencesBulkUpdate(
            dna_sequences=dna_sequences,
        )
