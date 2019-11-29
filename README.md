# Cassini Traceback

For [NaNoGenMo 2019](https://github.com/NaNoGenMo/2019/).

**Warning:** This README contains **flashing images**, and this project outputs a file that contains them.

How would a machine attempt to understand the actions of another machine, how would it tell the story of another machine?

_Cassini Traceback_ is one machine trying to make sense of the actions of the [_Cassini_](https://en.wikipedia.org/wiki/Cassini%E2%80%93Huygens) orbiter, whose incredible ~20-year mission ended with its atmospheric entry into Saturn. Taking as its starting point the [human-written accounts](https://solarsystem.nasa.gov/missions/cassini/mission/grand-finale/grand-finale-orbit-guide/) of its last orbits, the machine attempts to:

- parse the text related to each orbit, querying various sources for words and phrases that it doesn't recognise; and
- querying the amazing [OPUS datastore](https://tools.pds-rings.seti.org/opus/) for visual data sent back to Earth by _Cassini_ during that exact orbit, stitching it all into a single GIF.

The output is partly human-readable, partly machine-readable, studded throughout with image sequences originally captured millions of kilometers from Earth by a machine built by a group of primates from 28 different countries.

The program is only guaranteed to run on Python 3.7.x. Running it locally will take some time because of all of the network requests involved, and I have not implemented any rate limiting so please be respectful of the services involved. In addition to installing everything that's in the requirements file you will also need to run `python -m spacy download en_core_web_sm` before the program will work.

![Imaging Science Subsystem 2017-04-29T00:00:00.000–2017-05-06T00:00:00.000](272/ISS.gif)
