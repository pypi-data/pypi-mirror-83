from typing import List
from enum import Enum
from datetime import datetime

from spintop.models import (
    BaseDataClass,
    PersistenceIDRecord,
    OutcomeData,
    VersionIDRecord
)

class LCTypes():
    DUT = 'dut'
    STATION = 'station'
    OPERATOR = 'operator'
    SOFTWARE = 'software'
    STEP = 'step'

class LCUnit(VersionIDRecord):
    lc_type: str = ''

    @classmethod
    def from_version_id(cls, version_id, lc_type):
        return cls(
            id=version_id.id,
            version=version_id.version,
            lc_type=lc_type
        )

class LCStep(PersistenceIDRecord):
    outcome: OutcomeData = None
    duration: float = None
    lc_type: str = None # The lifecycle of this step. Linked with the units lc_types.
    units: List[LCUnit] = list
    filename: str = None
    pipeline_uuid: str = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.outcome is not None:
            self.outcome = OutcomeData.create(self.outcome)
