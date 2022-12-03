from dataclasses import dataclass
from typing import List, Union, Optional, Dict

@dataclass
class PGSupportedValue:
    value: Union[
        Union[str, int, float],
        List[Union[str, int, float]]
    ]

@dataclass
class PGTable:
    table: str

@dataclass
class PGColumn:
    column: str

@dataclass
class PGTarget:
    target: Dict[Union[str, int], Union[str, int]]






