from dataclasses import asdict
import json
from pathlib import Path
import shutil
from typing import Union

from rich.align import Align
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
import typer

from bud.bud_helpers import prompt_user, left_print
from bud.bud_types import Task

from bud import task
from bud import goal 

app = typer.Typer()
app.add_typer(task.app, name="task")
app.add_typer(goal.app, name = "goal")
console = Console()

PROJECT_CONFIG_DIR = Path(".bud")
PROJECT_CONFIG_FILE = Path(".bud/bud.toml")
TASK_DIR = Path(".bud/tasks")
TASK_FILE = Path(".bud/tasks/task.json")
GOAL_DIR = Path(".bud/goals")  
GOAL_FILE =Path(".bud/goals/goal.json")

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"


#def left_print(text, style: Union[str, None] = None, wrap: bool = False) -> None:
#    """Print text with center alignment.
#
#    Args:
#        text (Union[str, Rule, Table]): object to center align
#        style (str, optional): styling of the object. Defaults to None.
#    """
#    if wrap:
#        width = shutil.get_terminal_size().columns // 2
#    else:
#        width = shutil.get_terminal_size().columns
#
#    #console.print(Align.center(text, style=style, width=width))
#    console.print(Align.left(text, style=style, width=width))
#
#
#def prompt_user(prompt, fg_color = typer.colors.CYAN):
#    ''' Wrapper functions to prompt the user'''
#    return typer.prompt(typer.style(prompt, fg_color))



def get_task_dependencies() -> None:
    '''Prompt the user for dependencies'''
    return

@app.command()
def add( add_type: Annotated[str, typer.Argument()] )-> None:
    '''create a task'''

    if add_type == "task":
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

    for name, id in task_dict.keys():
        if task == name or (task in id):
            # Found the task to do
            task_dict[name].status = "Done"
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
        config.write(f"name = '{proj_name}'")
        config.write(f"username = '{username}'")

    left_print(f"Project {proj_name} made")
    return

def main() -> None:
    project_files = [PROJECT_CONFIG_DIR, 
                     PROJECT_CONFIG_FILE,
                     TASK_DIR,
                     TASK_FILE,
                     GOAL_DIR,
                     GOAL_FILE
                     ]

    # Check to see if there is a correct project dir
    if not all(x.exists() for x in project_files):
        print("No correct project dir")
        res = input("Would you like to make one?(y/n)")
        if res == 'n':
            return
        setup()

    # At this point there will be a project dir 
    app()


if __name__ == "__main__":
    main()

