# Copyright 2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""CLI commands"""

import json
import re
import shutil
from pathlib import Path

import click
import yaml

import zrtool
from zrtool import core, tool

# Context settings
CONTEXT_SETTINGS = {"auto_envvar_prefix": zrtool.PGRNAME.upper()}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=zrtool.__version__)
def main():
    """
    Manage ZoomR project and zrpa achive.

    To get help on a particular command run:

        zrtool COMMAND --help
    """


@main.command("archive", short_help="Create zrpa archive")
@click.option(
    "ask_pjtag",
    "--ask-project-tag/--no-project-tag",
    is_flag=True,
    default=False,
    help="Ask tags for the project.",
)
@click.option(
    "ask_ftag",
    "--ask-file-tag/--no-file-tag",
    is_flag=True,
    default=False,
    help="Ask tags for each audio file.",
)
@click.option(
    "compress",
    "--no-compress/--compress",
    is_flag=True,
    default=True,
    help=(
        "Compress means that wav file will be converted into flac file. "
        "By default it's compressed."
    ),
)
@click.option("--keep", "-k", is_flag=True, default=False)
@click.option(
    "metadataname",
    "--metadata",
    type=click.Path(exists=True),
    metavar="METADATAFILE",
    help="Path to a json or yaml file that will be used to read metadata.",
)
@click.argument("pjdir", type=click.Path(exists=True, file_okay=False))
@click.argument("zrpa", type=click.Path(dir_okay=False))
@click.pass_context
def archive(
    ctx, ask_pjtag, ask_ftag, compress, keep, metadataname, pjdir, zrpa
):
    """
    Create archive named ZRPA from project directory PJDIR.
    """
    pjdirpath = Path(pjdir).expanduser().resolve()
    arcpath = Path(zrpa).expanduser().resolve()
    # Ensure thate zrpa does not exist
    if arcpath.exists():
        click.confirm(
            "The file '{zrpa}' already exist. "
            "Do you want to overwrite it?".format(zrpa=zrpa),
            default=False,
            abort=True,
        )
    # Read metadata or create it
    metadata = {"project": {}, "audio": {}}
    if metadataname:
        metadatapath = Path(metadataname).expanduser().resolve()
        if metadatapath.suffix in (".yml", ".yaml"):
            with metadatapath.open("r") as yamlfile:
                metadata = yaml.safe_load(yamlfile.read())
        elif metadatapath.suffix == ".json":
            with metadatapath.open("r") as jsonfile:
                metadata = json.load(jsonfile)
        else:
            ctx.fail("Error: metadata file should be JSON or YAML.")
    # YAML file instruction
    instruction = (
        "# This is a regular yaml file.\n"
        "# Enter one tag per line as follow:\n"
        "# key: value\n"
        "# Example:\n"
        "# name: Name of this song\n"
        "# author: Me\n"
    )
    # Ask for project metadata
    if not metadataname and ask_pjtag:
        pjtag = "# Enter tags for the project\n#\n" + instruction
        pjtag_dict = tool.editmetadata(pjtag)
        metadata["project"] = tool.secure_usertag(pjtag_dict)
    # Ask for each file metadata
    if not metadataname and ask_ftag:
        for file in sorted((pjdirpath / "AUDIO").iterdir()):
            filetag = (
                "# Enter tags for file '{fname}'\n#\n".format(fname=file.name)
                + instruction
            )
            filetag_dict = tool.editmetadata(filetag)
            metadata["audio"][file.name] = tool.secure_usertag(filetag_dict)
    # Create zrpa file
    core.createzrpa(
        pjdir=pjdirpath, zrpa=arcpath, metadata=metadata, compress=compress
    )
    # Keep or delete the original file
    if not keep:
        shutil.rmtree(pjdirpath)


@main.command("export", short_help="Export zrpa archive to ZoomR format")
@click.option(
    "--number",
    metavar="N",
    nargs=1,
    type=int,
    help="The number of the project, if not specified it will be "
    "guessed looking at other project in the target directory.",
)
@click.option(
    "--with-tags/--without-tags",
    is_flag=True,
    default=False,
    help="Choose if metadata.json file should be exported or not.",
)
@click.argument("zrpa", type=click.Path(dir_okay=False))
@click.argument(
    "targetdir",
    type=click.Path(exists=True, file_okay=False),
    required=False,
    default=".",
)
@click.pass_context
def export(ctx, number, with_tags, targetdir, zrpa):
    """
    Export archive named ZRPA to a PROJNNN directory located in the
    current directory or if specified in target directory TARGETDIR.
    """
    # Define target directory
    targetdirpath = Path(targetdir).expanduser().resolve()
    # Define project name
    if not number:
        # Guess project name from taget directory
        number = 0
        for file in targetdirpath.iterdir():
            match = re.match(r"PROJ(?P<nb>\d{3})", file.name.upper())
            if match and int(match.group("nb")) >= number:
                number = int(match.group("nb")) + 1
    pjname = "PROJ{:03d}".format(number)
    pjdirpath = targetdirpath / pjname
    # Extract zrpa file
    try:
        core.exportzrpa(pjdir=pjdirpath, zrpa=zrpa, with_tags=with_tags)
    except FileExistsError as err:
        ctx.fail(err)
