import calendar
import inspect
import re
import traceback
from datetime import datetime


def get_traceback() -> str:
    """Format a traceback for HTML"""
    frame = inspect.currentframe()
    tb = traceback.extract_stack(frame).format()[:-2]
    tb = [line.replace("<module>", "&lt;module&gt;") for line in tb]
    return "<br/>        ".join([line.strip() for line in tb])


def format_date_string(start: str, finish: str) -> str:
    """Given two ISO 8601 date strings attempts to convert them into this format:
       Month Day–(Month) Day"""
    start_month, start_day = get_abbreviated_month_name_and_date(start)
    finish_month, finish_day = get_abbreviated_month_name_and_date(finish)

    start_string = f"{start_month} {start_day}"
    if finish_month != start_month:
        finish_string = f"{finish_month} {finish_day}"
    else:
        finish_string = f"{finish_day}"

    return f"{start_string}–{finish_string}"


def format_orbit_notes(text: str) -> str:
    """Given orbit notes returns them as HTML"""
    template = '<div class="orbit-notes"><p>{}</p></div>'
    html_text = text.replace("\n", "</p><p>")
    return template.format(html_text)


def get_abbreviated_month_name_and_date(date: str) -> tuple:
    """Given an ISO 8601 date string returns the abbreviated calendar month name
       and the date as a two-tuple"""
    date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return (calendar.month_abbr[date_obj.month], date_obj.day)


def parse_url(regex: str, url: str) -> str:
    """Returns the first match for `regex` in `url` or an empty string"""
    match = re.search(regex, url)
    return match[1] if match else ""
