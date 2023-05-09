from dataclasses import dataclass
from enum import Enum


class statusType(Enum):
   IDLE     = 1
   DEV      = 2
   DONE     = 3


@dataclass
class Task:
    name: str
    hash_id: str
    description: str
    duration: str
    depends_on: str
    status: str
    start_date: str



#@dataclass
#class milestone:
#    name: str
#    description: str
#    start_date: str
#    end_date: str
#    lvls: list[lvl]
#    status: str
#
#
#@dataclass
#class goal:
#    name: str
#    description: str
#    milestones: list[milestone]
