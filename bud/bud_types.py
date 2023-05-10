from dataclasses import dataclass
from enum import Enum


class statusType(Enum):
   IDLE     = 1
   DEV      = 2
   DONE     = 3

# hatchling
# growing
# done


@dataclass
class Task:
    name: str
    id: str
    description: str
    duration: str
    status: str
    start_date: str

@dataclass 
class Goal:
    name: str
    id: str
    description: str
    duration: str
    status: str
    start_date: str
    tasks: list[Task]


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
