import typer 
from bud.bud_types import Task
from bud.bud_helpers import left_print, prompt_user
from dataclasses import asdict
import json
from pathlib import Path
from typing_extensions import Annotated
from rich.table import Table

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
    status = "idea"
    start_date = ""
    id = str(abs(hash(name))) # @TODO Am I happy with ID generation?

    new_task = Task(
    name = name,
    id = id,
    description = desc,
    duration = duration,
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

@app.command(short_help="List tasks")
def show(verbose: Annotated[bool, typer.Option("--verbose", "-v")]= False )-> None:
    with open(TASK_FILE, 'r') as f:
        tasks = json.load(f)


    table1 = Table(
            title="Tasks",
            #title_style="grey39",
            title_style="blue",
            header_style="#e85d04",
            #header_style="orange",
            #style="#e85d04 bold",
            style="blue",
        )

    table1.add_column("Name")
    table1.add_column("Id")
    table1.add_column("Description")

    if verbose:
        table1.add_column("Duration")
        table1.add_column("Dependencies")
        table1.add_column("Status")
        table1.add_column("Start Date")
    
        # Load task 
        for _, details in tasks.items():
            task_obj = Task(**details)
            table1.add_row(
                    task_obj.name,
                    task_obj.id,
                    task_obj.description,
                    task_obj.duration,
                    task_obj.depends_on,
                    task_obj.status,
                    task_obj.start_date,
                    )
    else:
         # Load task 
        for _, details in tasks.items():
            task_obj = Task(**details)
            table1.add_row(
                    task_obj.name,
                    task_obj.id,
                    task_obj.description,
                    )

    left_print(table1)
    return




