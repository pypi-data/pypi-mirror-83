# Copyright 2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Core function"""

import json
import lzma
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

import invoke

from zrtool import FLACBIN, tool


def createzrpa(pjdir, zrpa, metadata, compress=True):
    """
    Create a zrpa archive from pjdir. pjdir must be root of a ZoomR
    project directory (e.g. PROJ000).

    :param pjdir: Path to ZoomR project directory (e.g. PROJ000).
    :type pjdir: Path
    :param zrpa: Path to the target zrpa file.
    :type zrpa: Path
    :param metadata: Dictionary containing metadata for the zrpa file.
    """
    invc = invoke.Context()
    with TemporaryDirectory() as tmpdirname:
        tmpdirpath = Path(tmpdirname)
        # Create audio directory
        (tmpdirpath / "audio").mkdir()
        # Convert wav to flac or compress them with xz
        for file in (pjdir / "AUDIO").iterdir():
            if file.suffix.lower() == ".wav" and compress:
                invc.run(
                    (
                        "{flacbin} "
                        "--best "
                        "--totally-silent "
                        "--keep-foreign-metadata "
                        "--output-name {output} "
                        "{input}"
                    ).format(
                        flacbin=FLACBIN,
                        input=file,
                        output=tmpdirpath / "audio" / (file.name + ".flac"),
                    )
                )
            else:
                xzfilepath = tmpdirpath / "audio" / (file.name + ".xz")
                with lzma.open(xzfilepath, "wb") as xzfile:
                    with file.open("rb") as source:
                        while True:
                            block = source.read(16)
                            if not block:
                                break
                            xzfile.write(block)
        # Create metadata json file
        metadatapath = tmpdirpath / "metadata.json"
        with metadatapath.open("w") as jsonfile:
            json.dump(metadata, jsonfile, indent=4)
        # Create root.tar.xz
        with tarfile.open(tmpdirpath / "root.tar.xz", "w:xz") as rootfile:
            rootfile.add(
                name=metadatapath,
                arcname=metadatapath.name,
                filter=tool.reset_uidgid,
            )
            for file in pjdir.iterdir():
                if (
                    file.name != "AUDIO"
                    and file.name != "metadata.json"
                    and file.name != "metadata.yml"
                ):
                    rootfile.add(
                        name=file, arcname=file.name, filter=tool.reset_uidgid
                    )
        # Create zrpa archive
        with tarfile.open(zrpa, "w:tar") as zrpafile:
            zrpafile.add(
                name=tmpdirpath / "audio",
                arcname="audio",
                filter=tool.reset_uidgid,
            )
            zrpafile.add(
                name=tmpdirpath / "root.tar.xz",
                arcname="root.tar.xz",
                filter=tool.reset_uidgid,
            )


def exportzrpa(pjdir, zrpa, with_tags=True):
    """
    Extract a zrpa archive to pjdir. pjdir will be root of a ZoomR
    project directory (e.g. PROJ000).

    :param pjdir: Path to ZoomR project directory (e.g. PROJ000).
    :type pjdir: Path
    :param zrpa: Path to the target zrpa file.
    :type zrpa: Path
    :param with_tags: Flag indicating to export the metadata file.
    :type with_tags: Boolean
    """
    invc = invoke.Context()
    # Create project directory
    pjdir.mkdir()
    # Extract zrpa file
    with tarfile.open(zrpa, "r:tar") as zrpafile:
        zrpafile.extractall(path=str(pjdir))
    # Convert audio files
    for file in (pjdir / "audio").iterdir():
        if file.suffix.lower() == ".flac":
            invc.run(
                (
                    "{flacbin} "
                    "--decode "
                    "--totally-silent "
                    "--keep-foreign-metadata "
                    "--output-name {output} "
                    "{input}"
                ).format(
                    flacbin=FLACBIN,
                    input=file,
                    # Getting old filename by removing ".flac"
                    output=pjdir / "audio" / file.name[:-5],
                )
            )
        else:
            # Getting old filename by removing ".xz"
            filepath = pjdir / "audio" / file.name[:-3]
            with filepath.open("wb") as dest:
                with lzma.open(file, "rb") as xzfile:
                    while True:
                        block = xzfile.read(16)
                        if not block:
                            break
                        dest.write(block)
        file.unlink()
    # Rename audio to AUDIO
    (pjdir / "audio").rename(pjdir / "AUDIO")
    # Extract root.tar.xz
    with tarfile.open(pjdir / "root.tar.xz") as rootfile:
        rootfile.extractall(pjdir)
    (pjdir / "root.tar.xz").unlink()
    if not with_tags:
        (pjdir / "metadata.json").unlink()
