import os
import pathlib

from analyse_images import analyse as analyse_images
from analyse_text import analyse as analyse_text
from helpers import format_date_string, format_orbit_notes, get_traceback
from log import get_logger


def analyse_orbit(orbit: dict) -> None:
    """Analyses the orbit data and logs it to the correct file"""

    directory = pathlib.Path(str(orbit["number"]))
    outpath = directory.joinpath("log.html")

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(outpath, "w") as fh:
        date_string = format_date_string(orbit["start"], orbit["finish"])
        intro_string = f"""
        <section>
            <h2>Orbit {orbit['number']} — {date_string}</h2>"""
        orbit_notes = format_orbit_notes(orbit["notes"])
        fh.write(intro_string + orbit_notes)

    logger = get_logger(__name__, outpath)
    logger.debug(
        "Analysing the text for orbit %s",
        orbit["number"],
        extra={"traceback": get_traceback()},
    )
    analyse_text(orbit["notes"], outpath)
    analyse_images(orbit, outpath)

    with open(outpath, "a") as fh:
        fh.write("</section>")
