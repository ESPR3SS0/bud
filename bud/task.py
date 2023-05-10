import typer 
from bud.bud_types import Task
from bud.bud_helpers import left_print, prompt_user
from dataclasses import asdict
import json
from pathlib import Path

PROJECT_CONFIG_DIR = Path(".bud")
PROJECT_CONFIG_FILE = Path(".bud/bud.toml")
TASK_DIR = Path(".bud/tasks")
TASK_FILE = Path(".bud/tasks/task.json")
GROUP_FILE = Path(".bud/tasks/groups.json")

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"


app = typer.Typer()

@app.command()
def add()-> None:
    '''create a task'''

    name = prompt_user("Task Name?")
    desc = prompt_user("Task Description?")
    duration = prompt_user("Duration?")
    deps = prompt_user("Depends on:")
    status = "idea"
    start_date = ""
    id = str(abs(hash(name))) # @TODO Am I happy with ID generation?

    new_task = Task(
    name = name,
    id = id,
    description = desc,
    duration = duration,
    depends_on = deps,
    status = status,
    start_date = start_date,
    )
    

    
    with open(TASK_FILE,'r+') as taskf:
        curlist = json.load(taskf)

    #curlist[name] = [desc,duration,dependencies,status,id]
    curlist[name] = asdict(new_task)

    with open(TASK_FILE,'w') as taskf:
        json.dump(curlist, taskf)

    left_print("Added new task", COLOR_SUCCESS)
    return


