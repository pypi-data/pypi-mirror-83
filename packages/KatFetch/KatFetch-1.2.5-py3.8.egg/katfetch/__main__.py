#!/usr/bin/python3

"""
KatFetch
Minimal and customizable information tool
By Kat Hamer
"""

import getpass  # Used to query user info
import os  # Used to query env variables
import pathlib  # Handle path objects
import platform  # Used to query OS info
import re  # Used to parse processor info
import shutil  # Used to check for wmctrl executable
import subprocess  # Used to run wmctrl

import click  # Command handler and color formatter
import distro  # Query Linux distro info
import hurry.filesize  # Display values in a human readable format
import psutil  # Query memory data

# List of valid Click style colors
TERM_COLORS = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "reset",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
]


def get_processor_name() -> str:
    """Get processor model name. This is hacky but is faster than cpuinfo and works on bsd"""
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        command = "/usr/sbin/sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).decode().strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    elif platform.system() == "OpenBSD":  # TODO test on other BSDs
        command = "sysctl hw.model"
        return (
            subprocess.check_output(command, shell=True)
            .decode()
            .strip()
            .replace("hw.model=", "")
        )
    return "Unknown"


def get_ram_info(value: str = "used") -> str:
    """
    Get used memory

    value (optional): a string representation of an attribute contained in a psutil.virtual_memory object
    """
    memory_object = psutil.virtual_memory()
    if hasattr(memory_object, value):
        memory_value = getattr(memory_object, value)
        human_readable = hurry.filesize.size(memory_value, system=hurry.filesize.si)
        return human_readable
    else:
        raise ValueError(
            f"Supplied memory value {value} is not a valid attribute of psutil.virtual_memory"
        )


def get_shell_version_string() -> str:
    """Get a version string representing the shell, e.g. bash 5.0"""
    shell_path_name = os.getenv("SHELL")  # Get $SHELL variable from environment
    if shell_path_name:
        shell_path = pathlib.Path(
            shell_path_name
        )  # Convert shell path into Path object
        shell_name = (
            shell_path.stem
        )  # Get last part of shell path. E.g. /bin/bash -> bash
        # Note, this looks a little messy because each shell has a different way of returning version
        if shell_name in ["fish", "tcsh"]:  # These provide no way to get version
            command_output = subprocess.check_output(
                [shell_path, "-c", "echo $version"]
            )  # Run the command with the specified shell
            version = command_output.decode().strip()
            return f"{shell_name} {version}"
        elif shell_name in ["zsh", "ksh", "bash"]:
            version_command = f"echo ${shell_name.upper()}_VERSION"  # Construct a command to echo the version name e.g. echo $ZSH_VERSION
            command_output = subprocess.check_output(
                [shell_path, "-c", version_command]
            )  # Run the command with the specified shell
            version = command_output.decode().strip()
            return f"{shell_name} {version}"
        else:  # For shells that provide no easy way to get version, e.g. sh, dash, ash
            return shell_name
    else:
        return "Unknown"


def get_wm() -> str:
    """Get current WM"""
    if shutil.which("wmctrl"):  # Check for wmctrl executable
        if os.getenv("DISPLAY"):  # Hacky check to see if we're inside an X server
            try:
                wm_info = subprocess.check_output(
                    ["wmctrl", "-m"]
                ).decode()  # Run wmctrl
                info_lines = wm_info.split("\n")
                wm = info_lines[0].replace("Name: ", "")  # Remove prefix from wm value
                return wm
            except Exception as e:
                print(f"get_wm: {e}")
                return "Unknown"
        else:
            return "N/A"
    else:
        return "Unknown"


def display_entry(title: str, value: str, accent: str = None):
    """
    Format and display a single data entry

    title: title of entry, will be accented
    value: value of entry
    accent (optional): click style color name, used for title
    """
    if accent:
        if accent in TERM_COLORS:
            title = click.style(title, fg=accent)
        else:
            raise ValueError(f"{accent} is not a valid color!")
    click.echo(f"{title} {value}")


def display_bar(length: int = 8, height: int = 2, block_width: int = 4):
    """
    Display a bar of colored blocks

    length: amount of colors to display
    height: height of bar
    block_width: width
    """
    for _ in range(height):
        for color in TERM_COLORS[:length]:
            click.secho(" " * block_width, bg=color, nl=False)
        print()  # Add a newline


def get_sysinfo() -> dict:
    """
    Get all system info

    returns a dictionary, each value is a lambda which when called provides the necessary data,
    this is done for performance reasons, so that each data element can be rendered at runtime
    """

    return {
        "OS": lambda: f"{platform.system()} {platform.release()}",
        "Hostname": lambda: platform.node(),
        "User": lambda: getpass.getuser(),
        "Shell": lambda: get_shell_version_string(),
        "Memory": lambda: get_ram_info("used") + "/" + get_ram_info("total"),
        "Terminal": lambda: os.getenv("TERM"),
        "Distro": lambda: distro.name(),
        "CPU": lambda: get_processor_name(),
        "WM": lambda: get_wm(),
    }


def display_all(accent: str = "blue"):
    """Display all values"""
    sys_info = get_sysinfo()
    for title, func in sys_info.items():
        display_entry(title, func(), accent)


@click.command()
@click.option("--bar/--no-bar", default=True, help="Whether or not to display bar")
@click.option("--just-bar/--not-just-bar", default=False, help="Display bar only")
@click.option(
    "--accent",
    default="blue",
    help="Accent color to use for highlighted entries, set to off for none",
)
@click.option("--bar-length", default=8, help="Amount of colors to display in bar")
@click.option("--bar-height", default=2, help="Height of bar")
@click.option("--stdout/--no-stdout", default=False, help="Output plaintext")
def main(bar, just_bar, accent, bar_length, bar_height, stdout):
    if just_bar:
        display_bar(bar_length, bar_height)
    else:
        if stdout:
            display_all(None)
        else:
            if accent:
                display_all(accent)
            else:
                display_al(None)
            if bar:
                display_bar(bar_length, bar_height)


if __name__ == "__main__":
    main()
