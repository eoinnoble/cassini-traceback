import asyncio
import logging
import pathlib

import aiohttp
import imageio
from aiohttp import ClientSession

from helpers import get_traceback, parse_url
from log import get_logger

INSTRUMENTS = {"CIRS", "ISS", "UVIS", "VIMS"}
ACRONYM_TO_INSTRUMENT_MAP = {
    "CIRS": "Composite Infrared Spectrometer",
    "ISS": "Imaging Science Subsystem",
    "UVIS": "Ultraviolet Imaging Spectrograph",
    "VIMS": "Visible and Infrared Mapping Spectrometer",
    "": "",
}
INSTRUMENT_REGEX = r"^.*Cassini\+([A-Z]*).*$"
START_REGEX = r"^.*time1=([0-9-T:.]*).*$"
END_REGEX = r"^.*time2=([0-9-T:.]*).*$"


def analyse(orbit: dict, outpath: pathlib.Path) -> None:
    """Runs all the image-related tasks"""
    logger = get_logger(__name__, outpath)

    asyncio.run(get_images_for_orbit(orbit, outpath, logger))


async def fetch_opus_json(
    *, url: str, session: ClientSession, logger: logging.Logger
) -> dict:
    """GET request wrapper to fetch JSON from OPUS"""
    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    logger.info(
        "Got response [%s] for URL: %s",
        resp.status,
        f'<a href="{url}">{url}</a>',
        extra={"traceback": get_traceback()},
    )
    return await resp.json()


async def parse_image_urls_from_opus_data(
    *, url: str, session: ClientSession, logger: logging.Logger
) -> list:
    """Find image URLs in OPUS JSON"""
    try:
        logger.debug("Fetching OPUS JSON", extra={"traceback": get_traceback()})
        opus_data = await fetch_opus_json(url=url, session=session, logger=logger)
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
            extra={"traceback": get_traceback()},
        )
        return []
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s",
            getattr(e, "__dict__", {}),
            extra={"traceback": get_traceback()},
        )
        return []
    else:
        image_urls = [image["path"] + image["img"] for image in opus_data["data"]]
        urls_for_log = [f'<a href="{url}">{url}</a>' for url in image_urls]
        logger.info(
            "Found %s image URLs: %s",
            len(urls_for_log),
            urls_for_log,
            extra={"traceback": get_traceback()},
        )
        return image_urls


async def write_cassini_images_to_file(
    *, file: pathlib.Path, url: str, session: ClientSession, logger: logging.Logger
) -> None:
    """Write the found images from `url` to `file`."""
    image_urls = await parse_image_urls_from_opus_data(
        url=url, session=session, logger=logger
    )

    if not image_urls:
        return None

    with imageio.get_writer(file, mode="I") as writer:
        logger.debug(f"Writing images to {file}", extra={"traceback": get_traceback()})
        for image_url in image_urls:
            writer.append_data(imageio.imread(image_url))

    instrument_name = ACRONYM_TO_INSTRUMENT_MAP[parse_url(INSTRUMENT_REGEX, url)]
    start_time = parse_url(START_REGEX, url)
    end_time = parse_url(END_REGEX, url)
    caption_string = (
        f"<figcaption>{instrument_name}<br/>{start_time}–{end_time}</figcaption>"
    )

    msg = f'<figure class="opus-gif"><img src="{file}"/>{caption_string}</figure>'
    logger.debug(msg, extra={"traceback": get_traceback()})


async def get_images_for_orbit(
    orbit: dict, outpath: pathlib.Path, logger: logging.Logger
) -> None:
    """Schedules the tasks for fetching images related to this orbit"""
    request_template = (
        "https://tools.pds-rings.seti.org/opus/api/images/small.json"
        "?instrument=Cassini+{}"
        "&time1={}"
        "&time2={}"
    )

    async with ClientSession() as session:
        tasks = []

        for instrument in INSTRUMENTS:
            if instrument in orbit["notes"]:
                url = request_template.format(
                    instrument, orbit["start"], orbit["finish"]
                )

                file = outpath.parent.joinpath(f"{instrument}.gif")

                tasks.append(
                    write_cassini_images_to_file(
                        file=file, url=url, session=session, logger=logger
                    )
                )
        await asyncio.gather(*tasks)
