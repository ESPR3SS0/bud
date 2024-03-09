# Need this to read toml, also in standard lib
import tomllib 

from datetime import datetime

import polars as pl

# Need this to write to toml
import typer

from bud import task
from bud import goal 

import zoneinfo
from rich.align import Align
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from typing_extensions import Annotated
import typer
from pathlib import Path


app = typer.Typer(pretty_exceptions_show_locals=False)

PROJECT_CONFIG_DIR = Path(".bud")
PROJECT_CONFIG_FILE = Path(".bud/bud.toml")
TASK_DIR = Path(".bud/tasks")
TASK_FILE = Path(".bud/tasks/task.json")
TASK_LOG_FILE = Path(".bud/tasks/task_log.json")
GOAL_DIR = Path(".bud/goals")  
GOAL_FILE =Path(".bud/goals/goal.json")

TIME_FILE = Path(".bud/time.csv")

COLOR_INFO = "cyan1 on purple3"
COLOR_SUCCESS = "black on green"
COLOR_WARNING = "bright_red on bright_white"
COLOR_ERROR = "black on bright_red"



def read_clocks():
    '''
    Read the clock hours
    '''
    # If the file doesn't exist create it 
    if not TIME_FILE.exists():
        time_df = pl.DataFrame({})#, schema=schema)
    else:
        time_df = pl.read_csv(TIME_FILE)
    return time_df







@app.command(short_help="Read Clocks")
def hours(
        day: Annotated[str,typer.Argument(
            help="Display total hours for today")] = None,
        week: Annotated[str,typer.Argument(
            help="Displayu the hours for this week")] = None,
        month: Annotated[str,typer.Argument(
            help="Display hours for this month")] = None,
    ): 
    '''
    REad the hours for in the clock
    '''



    return


@app.command()
def clock(
        reset: Annotated[bool,typer.Option("-r", "--reset", 
            help='Clear the most recent clock in and reset')] = False,
        status: Annotated[bool,typer.Option("-s", "--status", 
            help="Display if currently clocked in or out")] = False,
        list: Annotated[bool,typer.Option( 
            help="List the past 5 clocks")] = False,
    ):
    """Toggle a time clock

    """

    # Schema was not working well when trying to read a csv
    #schema = {
    #    "date" : pl.Date,
    #    "time" : pl.Time,
    #    "datetime" : pl.Datetime,
    #    "clock_in" : bool,
    #    "clock_out" : bool
    #}
    time_df = read_clocks()

    if reset:
        print("In reset")
        # Pop the most 

        time_df = time_df.with_columns(pl.col('datetime').str.to_datetime("%Y-%m-%d %H:%M:%S%.f").alias("pdatetime"))
        # Sort the DataFrame by the 'Date' column in descending order
        time_df = time_df.sort('pdatetime', descending=True)
        most_recent_time = time_df['pdatetime'][0]
        print(f"Most recent time was: {most_recent_time}")

        # Confirm with the user they want to remove the last clock
        conf = input("Confirm remove(y/Y")
        if conf in ['y', 'Y']:
            time_df = time_df.filter(pl.col('pdatetime') != most_recent_time)


    # Get the row with the most recent time
    time_df = time_df.with_columns(pl.col('datetime').str.to_datetime("%Y-%m-%d %H:%M:%S%.f").alias("pdatetime"))

    # Sort the DataFrame by the 'Date' column in descending order
    latest_action = time_df.sort('pdatetime', descending=True)
    was_clock_in = latest_action['clock_in'][0]

    # Toggle the clock 
    if was_clock_in:
        action = 'out'
    else:
        action = 'in'

    print(f"Clocking {action}")

    # Drop the pdatetime clock
    time_df = time_df.drop("pdatetime")

    # Get the current time
    current_time = datetime.utcnow()

    # Get the times
    data = {
        "date" : str(current_time.date()),
        "time" : str(current_time.time()),
        "datetime" : str(current_time),
        "clock_in" : True if action=="in" else False,
        "clock_out" : True if action=="out" else False,
    }

    # Create the new dataframe
    df2 = pl.DataFrame(data) #, schema=schema)

    time_df = pl.concat([time_df, df2])


    if list:
        print("Previous 5 entries...")
        print(time_df.tail(5))

    # Write the to the time file
    time_df.write_csv(TIME_FILE)
    return
