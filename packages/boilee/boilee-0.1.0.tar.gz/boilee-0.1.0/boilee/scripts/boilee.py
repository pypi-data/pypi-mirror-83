from inspect import Parameter
from jinja2 import Template
from PyInquirer import prompt, Separator
import click
import json
import yaml
import tempfile
import zipfile
import docopt

from boilee.database import Database


def default_values(parameter):
    if parameter["type"] == "input":
        return {
            **parameter,
            **{"parameter_type": "option", "default": None, "ask_in": "all",},
        }
    elif parameter["type"] == "confirm":
        return {**parameter, **{"default": False, "ask_in": "all", "help": None}}
    elif parameter["type"] in ["list", "rawlist"]:
        return {
            **parameter,
            **{"parameter_type": "option", "ask_in": "all", "help": None},
        }
    elif parameter["type"] == "checkbox":
        parameter["choices"] = map(
            lambda choice: {**choice, **{"checked": False}}, parameter["choices"]
        )
        return {
            **parameter,
            **{"parameter_type": "option", "ask_in": "all", "help": None},
        }


@click.group()
def cli():
    pass


@cli.command()
@click.argument("src")
@click.argument("dst")
def make(src, dst):
    zipfile.ZipFile(dst, "w")
    temp_dir = tempfile.TemporaryDirectory()
    database = Database(temp_dir)

    try:
        parameters = yaml.load(
            json.loads(open(f"{src}/.boilee/arguments.yml", "r").read()),
            Loader=yaml.FullLoader,
        )

        parameters = {
            parameters[key]: default_values(value) for key, value in parameters
        }
    except FileNotFoundError:
        parameters = None

    docopt_usage = f"    boilee run <src> <dst>"
    docopt_options = "    -h --help     Show this screen.\n"

    inquirer_answers = []
    inquire_nonused_parameters = ["help"]

    for key, value in parameters:

        if value["ask_in"] != "after_init":
            if "help" not in value:
                value["help"] = None

            if value["type"] == "input":
                if value["type_parameter"] == "argument":
                    docopt_usage = (
                        f"{docopt_usage} {f'<{key}>' if value['required'] else f'[<{key}>]'}"
                    )
                else:
                    docopt_usage = f"{docopt_usage} {f'--{key}=<{key}>' if value['required'] else f'[--{key}=<{key}>]'}"
                    docopt_options = f"{docopt_options} --{key}=<{key}>    {value['help']}\n"

                inquirer_answers.append(value)

            elif value["type"] in ["list", "rawlist"]:
                choices_list = [
                    f"{choice['message']}\n"
                    for choice in value["choices"]
                    if not "separator" in choice
                ]
                choices = "".join(choices_list).replace("\n", "|")[:-1]
                docopt_usage = f"{docopt_usage} {f'--{key}=({choices})' if value['required'] else f'[--{key}=({choices})]'}"
                docopt_options = f"{docopt_options} --{key}={key}    {value['help']}\n"

            elif value["type"] == "confirm":
                docopt_usage = f"{docopt_usage} --{key}"
                docopt_options = f"{docopt_options} --{key}    {value['help']}\n"

            elif value["type"] == "checkbox":
                #TODO: Add checkbox for docopt parameters
                pass
