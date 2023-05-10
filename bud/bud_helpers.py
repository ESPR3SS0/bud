
from typing import Union
import typer
import shutil
from rich.console import Console
from rich.align import Align

console = Console()

def left_print(text, style: Union[str, None] = None, wrap: bool = False) -> None:
    """Print text with center alignment.

    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """
    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    #console.print(Align.center(text, style=style, width=width))
    console.print(Align.left(text, style=style, width=width))



def prompt_user(prompt, fg_color = typer.colors.CYAN):
    ''' Wrapper functions to prompt the user'''
    return typer.prompt(typer.style(prompt, fg_color))

