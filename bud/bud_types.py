from dataclasses import dataclass
from enum import Enum


class Status(Enum):
   IDLE     = 'IDLE'
   DEV      = 'DEV'
   DONE     = 'DONE'

# hatchling
# growing
# done


class Priority(Enum):
    HIGHEST     = "HIGHEST"
    HIGH        = "HIGH"
    MODERATE    = "MODERATE"
    LOW         = "LOW"
    LOWEST      = "LOWEST"



@dataclass
class Task:
    name: str
    id: str
    description: str
    duration: str
    status: str
    priority: str
    start_date: str

@dataclass 
class Goal:
    name: str
    id: str
    description: str
    duration: str
    status: str
    start_date: str
    priority: str
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
