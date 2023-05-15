from dataclasses import asdict
import json
from pathlib import Path
import shutil
from typing import Union, List

import sys, os
from subprocess import call

from rich.align import Align
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
import typer

from bud.bud_helpers import prompt_user, left_print, center_print
from bud.bud_types import Task, Goal, Status, Priority

from bud import task
from bud import goal 

import random

# Need this to read toml, also in standard lib
import tomllib 

import datetime

# Need this to write to toml
import toml 

app = typer.Typer()
app.add_typer(task.app, name="task")
app.add_typer(goal.app, name = "goal")
console = Console()

PROJECT_CONFIG_DIR = Path(".bud")
PROJECT_CONFIG_FILE = Path(".bud/bud.toml")
TASK_DIR = Path(".bud/tasks")
TASK_FILE = Path(".bud/tasks/task.json")
TASK_LOG_FILE = Path(".bud/tasks/task_log.json")
GOAL_DIR = Path(".bud/goals")  
GOAL_FILE =Path(".bud/goals/goal.json")

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"


if os.environ.get('EDITOR'):
    EDITOR = os.environ.get('EDITOR')  
else:
    EDITOR = 'vi'


def get_task_dependencies() -> None:
    '''Prompt the user for dependencies'''
    return


def getconfig():
    '''
        Function to read the local config file
    '''

    with open(PROJECT_CONFIG_FILE, 'rb') as f:
        data = tomllib.load(f)

    return data


# This is copied from please, and shows how please handled 
# quotes 
def getquotes() -> dict:
    """Select a random quote.

    Returns:
        dict: quote with its metadata
    """

    with open(config["quotes_file"], "r") as qf:
        quotes_file = json.load(qf)
    return quotes_file[random.randrange(0, len(quotes_file))]


@app.callback(invoke_without_command=True)
def nocommand(context: typer.Context)->None:
    '''
        Run the show command by default
    '''

    # If a command was passed leave this function
    if context.invoked_subcommand is not None:
        return



    # This is a line from please that prints a quote
    # quote = getquotes()
    #center_print(f'[#63D2FF]"{quote["content"]}"[/]', wrap=True)
    config = getconfig()
    user_name = config['proj_info']['username']

    # This is a line from pleadse that prints hello and the time
    date_text = f"[#FFBF00] Hello {user_name}! It's {datetime.datetime.now().strftime('%d %b | %I:%M %p')}[/]"
    center_print(date_text)

    show()
    return


#def add( add_type: Annotated[str, typer.Argument()] = "task" )-> None:
#def add(name: Annotated[str, typer.Argument("-n", "--name" )] = None,
@app.command()
def add(ctx: typer.Context,
        name: Annotated[str, typer.Argument()] = None,
        duration: Annotated[str,typer.Option("-u", "--duration")] = None,
        priority: Annotated[str,typer.Option("-p", "--priority" )] = None,
        provide_description: Annotated[bool, typer.Option("-d", "--description")] = None,
        )-> None:
    '''By deafult the only required field is going to be the name'''

    #description: Annotated[List[str], typer.Option("-d", "--description", prompt=True)]

    # Get the task name 
    if name is None:
        name = prompt_user("Task Name(SingleWord)?")
        while " " in name:
            name = prompt_user("Task Name(Must be SingleWord)?")

    if duration is None:
        duration = ""

    if priority is None:
        priority = Priority.LOWEST.name

    if provide_description == True:
        desc = prompt_user("Task Description?")
    else:
        desc = ""

    status = Status.IDLE.name
    start_date = str(datetime.datetime.now())
    id = str(abs(hash(name))) # @TODO Am I happy with ID generation?
    #left_print("Priority(HIGH(EST)-MODERATE-LOW(EST)?")
    #priority = prompt_user("Priority?")
    #if priority not in ["HIGHEST", "HIGH", "MODERATE", "LOW","LOWEST"]:
    #    priority = ""


    new_task = Task(
        name = name,
        id = id,
        priority = priority,
        description = " ".join(desc),
        duration = duration,
        status = status,
        start_date = start_date,
    )

    
    with open(TASK_FILE,'r+') as taskf:
        curlist = json.load(taskf)

    curlist[name] = asdict(new_task)

    with open(TASK_FILE,'w') as taskf:
        json.dump(curlist, taskf)

    left_print("Added new task", COLOR_SUCCESS)
    return


@app.command(short_help="Do a task [id, partial id, name]")
def do(task: str) -> None:

    # Accept either id, partial  id, or name 

    with open(TASK_FILE,'r') as taskin:
        task_dict = json.load(taskin)

    for task_name, task_items in task_dict.items():
        #if task == task_name or (task in id):

        if task == task_name:

            loaded_task = Task(**task_items)

            loaded_task.status = Status.DONE.name

            task_dict[task_name] = asdict(loaded_task)

            with open(TASK_FILE,'w') as taskf:
                json.dump(task_dict, taskf)

            return


@app.command(short_help="Earse a task")
def remove(task: str):
    '''
        Completely remove a task
    '''
    with open(TASK_FILE,'r') as taskin:
        task_dict = json.load(taskin)

    if task in task_dict.keys():
        task_dict.pop(task)
        left_print(f"Removed item: {task}")


    with open(TASK_FILE,'w') as taskf:
        json.dump(task_dict, taskf)

    #for name, id in task_dict.items():
    #    if task == name or (task in id):
    #        # Found the task to do
    #        removed_item = task_dict.pop(name)
    return

@app.command(short_help="Scratch")
def scratch(pad_name:Annotated[str, typer.Option()])-> None:

    

    return




@app.command(short_help="List goals and tasks")
def show(verbose: Annotated[bool, typer.Option("--verbose", "-v")]= False )-> None:


    # For now Im going to make a table with the following format

    #  Task x 

    with open(TASK_FILE, 'r') as f:
        tasks = json.load(f)

    config = getconfig()
    proj_name = config["proj_info"]["name"]

    table1 = Table(
            title=proj_name,
            #title_style="grey39",
            title_style="blue",
            header_style="#e85d04",
            #header_style="orange",
            #style="#e85d04 bold",
            style="blue",
        )

    table1.add_column("Task Name")
    table1.add_column("Duration")
    table1.add_column("Start Date")
    table1.add_column("Status")
    table1.add_column("Priority")
    table1.add_column("Goal")

    # Need to be able to put down the goal that a task is apart of 
    # Need a list of goal and there tasks 

    goalList = []

    with open(GOAL_FILE, 'r') as goalf:
        goalList = json.load(goalf)

    task_goal_dict = {}

    for _, cur_goal in goalList.items():
        goal = Goal(**cur_goal)
        if goal.tasks != []:
            for cur_task in goal.tasks:
                task = Task(**cur_task)
                if task.name not in task_goal_dict.keys():
                    task_goal_dict[task.name] = [goal.name]
                else:
                    task_goal_dict[task.name].append(goal.name)

    for _ , details in tasks.items():
        if "priority" not in details.keys():
            details['priority'] = ""
        task_obj = Task(**details)
        if task_obj.name not in task_goal_dict.keys():
            task_goal_dict[task_obj.name] = []

        table1.add_row(
                task_obj.name,
                task_obj.duration,
                task_obj.start_date,
                task_obj.status,
                task_obj.priority,
                " ".join(task_goal_dict[task_obj.name])
                )

    left_print(table1)
    return

#@app.command(short_help="Get quotes")
#def quote():
#    with open("quotes.json", "r") as qf:
#        quotes_file = json.load(qf)
#    return quotes_file[random.randrange(0, len(quotes_file))]


@app.command(short_help="Log the saved tasks and remove from show table")
def log():
    '''
        log 

        Any tasks that are marked as done will be saved to a log file 
        and no longer appear in the task table
    '''

    # Open the task file 
    with open(TASK_FILE,'r+') as taskf:
        raw_file = json.load(taskf)

    names_to_remove = []
    
    # Find all the tasks that are marked as DONE
    for task_name, task_items in raw_file.items():
        cur_task = Task(**task_items)
        
        if cur_task.status == Status.DONE.name:
            names_to_remove.append(task_name)

    # Open the current task log file 
    with open(TASK_LOG_FILE, 'r') as logf:
        logged_raw = json.load(logf)

    # Add the new items to the log file
    for task_name in names_to_remove:
        item = raw_file.pop(task_name)
        logged_raw[task_name] = item
    
    # Save the new log file 
    with open(TASK_LOG_FILE, 'w') as logf:
        json.dump(logged_raw, logf)
    
    # Save the new json document with the removed tasks
    with open(TASK_FILE,'w') as taskf:
        json.dump(raw_file, taskf)

    return



@app.command(short_help="Init new project")
def setup():
    '''Init a new project'''

    typer.style("Creating new projet!", fg=typer.colors.CYAN)

    username = prompt_user("Hello! What can I call you?")
    left_print(f"\nHey there {username}!")

    proj_name= prompt_user("Project Name?")

    # Make the directory and file
    PROJECT_CONFIG_DIR.mkdir(exist_ok=True)
    PROJECT_CONFIG_FILE.touch(exist_ok=True)
    TASK_DIR.mkdir(exist_ok=True)
    GOAL_DIR.mkdir(exist_ok=True)

    with open(TASK_FILE, "w") as f:
        json.dump({}, f)

    with open(GOAL_FILE, "w") as f:
        json.dump({}, f)

    #TASK_FILE.touch(exist_ok=True) 

    with open(PROJECT_CONFIG_FILE, "r+") as config:
        config.write("[proj_info]")
        config.write(f"\nname = '{proj_name}'")
        config.write(f"\nusername = '{username}'")

    left_print(f"Project {proj_name} made")
    return

def main() -> None:
    project_files = [PROJECT_CONFIG_DIR, 
                     PROJECT_CONFIG_FILE,
                     TASK_DIR,
                     TASK_FILE,
                     GOAL_DIR,
                     GOAL_FILE,
                     TASK_LOG_FILE
                     ]

    # Check to see if there is a correct project dir
    if not all(x.exists() for x in project_files):

        # Make a list of missing files
        missing_files = [x for x in project_files if x.exists() == False]

        # Check to see if this directory had a .bud file
        if Path(".bud").exists():
            print("Malformed bud project, the .bud directoty is missing the following necessary files:")
            print(" ".join([x.name for x in missing_files]))
            res = input("Would you like to touch only the missing files?(y/Y/n/N)")
            if res == 'y' or res == 'Y':
                for missing_file in missing_files:

                    if missing_file.is_dir():
                        missing_file.mkdir(exist_ok=True)
                    else:
                        with open(missing_file, "w") as f:
                            json.dump({}, f)

        else:

            res = input("Would you like to init a bud project?(y/n)")
            if res == 'n':
                return
            setup()

    # At this point there will be a project dir 
    app()


if __name__ == "__main__":
    main()

