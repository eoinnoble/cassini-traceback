import logging
import pathlib
import warnings
from typing import Set

import spacy
import wikipedia
from nltk.corpus import words
from wiktionaryparser import WiktionaryParser

from helpers import get_traceback
from log import get_logger

NLP = spacy.load("en_core_web_sm")
PARSER = WiktionaryParser()

ORGS = set()
KNOWN: Set[str] = set()
UNKNOWN: Set[str] = set()


def analyse(text: str, outpath: pathlib.Path) -> None:
    """Runs all text-related tasks"""
    logger = get_logger(__name__, outpath)

    logger.debug(
        "Analysing orbit text with spaCy", extra={"traceback": get_traceback()}
    )
    doc = NLP(text)

    for ent in doc.ents:
        if (
            ent.label_ == "ORG"
        ):  # Most of the nouns we care about get classified as 'ORG'
            logger.debug(f"Found {ent.text}", extra={"traceback": get_traceback()})
            ORGS.add(ent.text)

            safe_text = ent.text.lower()

            if safe_text in KNOWN or safe_text in words.words():
                logger.debug(
                    "I know what %s means, I have seen it before",
                    ent.text,
                    extra={"traceback": get_traceback()},
                )
                continue
            elif safe_text in UNKNOWN:
                logger.debug(
                    "I have seen %s before but can't work out what it means",
                    ent.text,
                    extra={"traceback": get_traceback()},
                )
                continue
            else:
                query_wikipedia(query=safe_text, logger=logger)
                if safe_text in UNKNOWN:  # Wikipedia was not helpful, try Wiktionary
                    query_wiktionary(query=safe_text, logger=logger)


def query_wikipedia(*, query: str, logger: logging.Logger, sentences: int = 10) -> None:
    """Log a Wikipedia summary of length `sentences` for the given `query` or
       raise an error"""
    try:
        logger.debug(
            "Searching Wikipedia for %s", query, extra={"traceback": get_traceback()}
        )
        # The wikipedia package has not configured bs4 correctly and causes a warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            summary = wikipedia.summary(query, sentences=sentences)
    except (
        wikipedia.exceptions.DisambiguationError,
        wikipedia.exceptions.PageError,
    ) as e:
        logger.error(
            "Encountered an error searching Wikipedia for %s: %s",
            query,
            e,
            extra={"traceback": get_traceback()},
        )
        UNKNOWN.add(query)
    else:
        logger.info(
            "Found summary information for %s: %s",
            query,
            summary,
            extra={"traceback": get_traceback()},
        )
        KNOWN.add(query)


def query_wiktionary(*, query: str, logger: logging.Logger) -> None:
    """Log a definition from Wiktionary for a given `query`"""
    logger.debug(
        "Searching Wiktionary for %s", query, extra={"traceback": get_traceback()}
    )
    word = PARSER.fetch(query)

    if len(word[0]["definitions"]):
        logger.info(
            "Found definitions for %s: %s",
            query,
            [definition["text"] for definition in word[0]["definitions"]],
            extra={"traceback": get_traceback()},
        )
        KNOWN.add(query)
    else:
        logger.info(
            "Found nothing in Wiktionary for %s",
            query,
            extra={"traceback": get_traceback()},
        )
        UNKNOWN.add(query)
