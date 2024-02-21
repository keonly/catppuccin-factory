#!/usr/bin/env python3
import signal
import argparse
import sys
import os
from pathlib import Path

from ImageGoNord import GoNord

from rich.console import Console
from rich.panel import Panel

# CHANGE pirate TO YOUR OWN USER NAME, DO NOT CHANGE THE DIRECTORY ITSELF
mypath = "/home/keon/Pictures/cat/"


def main():

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()

    cat_factory = GoNord()
    cat_factory.reset_palette()
    add_cat_palette(cat_factory)

    # Checks if there's an argument
    if len(sys.argv) > 1:
        image_paths = fromCommandArgument(console)
    else:
        image_paths = fromTui(console)

    for image_path in image_paths:
        if os.path.isfile(image_path):
            process_image(image_path, console, cat_factory)
        else:
            console.print(
                f"❌ [red]We had a problem in the pipeline! \nThe image at '{image_path}' could not be found! \nSkipping... [/]"
            )
            continue


# Gets the file path from the Argument
def fromCommandArgument(console):
    command_parser = argparse.ArgumentParser(
        description="A simple cli to manufacture Catppuccin themed wallpapers."
    )
    command_parser.add_argument(
        "Path", metavar="path", nargs="+", type=str, help="The path(s) to the image(s)."
    )
    args = command_parser.parse_args()

    return args.Path


# Gets the file path from user input
def fromTui(console):

    console.print(
        Panel(
            "🏭 [bold magenta] Catppuccin Factory [/] 🏭",
            expand=False,
            border_style="magenta",
        )
    )

    return [
        os.path.expanduser(path)
        for path in console.input(
            "🖼️ [bold yellow]Which image(s) do you want to manufacture? (image paths separated by spaces):[/] "
        ).split()
    ]


def process_image(image_path, console, cat_factory):
    image = cat_factory.open_image(image_path)

    console.print(f"🔨 [blue]manufacturing '{os.path.basename(image_path)}'...[/]")

    # TODO: might be a better idea to save the new Image in the same directory the command is being run from
    save_path = os.path.join(mypath, "cat_" + os.path.basename(image_path))

    cat_factory.convert_image(image, save_path=(save_path))
    console.print(f"✅ [bold green]Done![/] [green](saved at '{save_path}')[/]")


def add_cat_palette(cat_factory):

    catPalette = [
        "#F2CDCD",
        "#DDB6F2",
        "#F5C2E7",
        "#E8A2AF",
        "#F28FAD",
        "#F8BD96",
        "#FAE3B0",
        "#ABE9B3",
        "#B5E8E0",
        "#96CDFB",
        "#89DCEB",
        "#161320",
        "#1A1826",
        "#161616",
        "#302D41",
        "#575268",
        "#6E6C7E",
        "#988BA2",
        "#C3BAC6",
        "#D9E0EE",
        "#C9CBFF",
        "#F5E0DC",
    ]

    for color in catPalette:
        cat_factory.add_color_to_palette(color)


## handle CTRL + C
def signal_handler(signal, frame):
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
