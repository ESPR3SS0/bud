import typer 
from bud.bud_types import Task, Goal
from bud.bud_helpers import left_print, prompt_user
from dataclasses import asdict
import json
from pathlib import Path
from rich.table import Table


PROJECT_CONFIG_DIR = Path(".bud")
PROJECT_CONFIG_FILE = Path(".bud/bud.toml")
TASK_DIR = Path(".bud/tasks")
TASK_FILE = Path(".bud/tasks/task.json")
GOAL_DIR = Path(".bud/goals")  
GOAL_FILE =Path(".bud/goals/goal.json")
GROUP_FILE = Path(".bud/tasks/groups.json")

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"


app = typer.Typer()

@app.command()
def add()-> None:
    '''create a goal'''

    name = prompt_user("Goal Name?")
    desc = prompt_user("Goal Description?")
    duration = prompt_user("Duration?")
    deps = prompt_user("Depends on:")
    status = "idea"
    start_date = ""
    id = str(abs(hash(name))) # @TODO Am I happy with ID generation?

    # Load the current tasks
    with open(TASK_FILE, 'r') as f:
        tasks = json.load(f)

    # Need all the task names
    all_task_names = [x for x,_ in tasks.items()]
    print(all_task_names)
    

    # Save a list of add tasks
    goal_tasks = []

    # Need to get a list of tasks
    done = False
    while not done:

        # Get the task name to add to the list of tasks
        task_name= prompt_user("task name (NONE)")

        if task_name == "NONE":
            break

        # See if the task name is valid
        if task_name not in all_task_names:
            print(f"Task doesn't exist: {task_name}")
            continue

        goal_tasks.append(tasks[task_name])

    new_goal= Goal(
        name = name,
        id = id,
        description = desc,
        duration = duration,
        status = status,
        start_date = start_date,
        tasks = goal_tasks
    )
    

    
    with open(GOAL_FILE,'r+') as goalf:
        curlist = json.load(goalf)

    #curlist[name] = [desc,duration,dependencies,status,id]
    curlist[name] = asdict(new_goal)

    with open(GOAL_FILE,'w') as goalf:
        json.dump(curlist, goalf)

    left_print("Added new goal", COLOR_SUCCESS)
    return

@app.command()
def show():
    with open(GOAL_FILE, 'r') as f:
        goal = json.load(f)


    table1 = Table(
            title="Goals",
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
    table1.add_column("Tasks")

         # Load task 
    for _, details in goal.items():
        goal_obj = Goal(**details)

        table1.add_row(
                goal_obj.name,
                goal_obj.id,
                goal_obj.description,
                "\n".join([Task(**x).name for x in goal_obj.tasks])
                )

    left_print(table1)
    return






