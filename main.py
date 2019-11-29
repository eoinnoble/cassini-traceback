import json

from bs4 import BeautifulSoup as soup

from orbit import analyse_orbit

if __name__ == "__main__":
    with open("orbits.json", "r") as fh:
        data = json.load(fh)
        orbits = data["orbits"]

    final_output_template = """
    <html>
        <head>
            <title>Cassini traceback</title>
            <link href="https://fonts.googleapis.com/css?family=Fira+Sans:400,900&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css?family=Fira+Mono&display=swap" rel="stylesheet">
            <link href="styles.css" rel="stylesheet">
        </head>
        <body>
            <h1>Cassini Traceback</h1>
            {}
            <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/xrGAQCq9BMU?start=166&mute=1" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </body>
    </html>"""
    all_logs = ""

    for orbit in orbits:
        analyse_orbit(orbit)
        with open(f'{orbit["number"]}/log.html', "r") as fh:
            all_logs += fh.read()

    # analyse_orbit(orbits[0])

    # with open(f'{orbits[0]["number"]}/log.html', 'r') as fh:
    #     all_logs += fh.read()

    # for i in range(5):
    #     analyse_orbit(orbits[i])
    #     with open(f'{orbits[i]["number"]}/log.html', 'r') as fh:
    #         all_logs += fh.read()

    with open("app.html", "w") as fh:
        html = soup(final_output_template.format(all_logs), features="html.parser")
        fh.write(html.prettify())
