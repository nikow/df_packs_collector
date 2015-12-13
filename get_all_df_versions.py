#!/usr/bin/python3 -uBdOO

import os
import re
import urllib
import urllib.request

print("Parsing config...")
link_template = "http://www.bay12games.com/dwarves/%s"
download_command = "wget -c \"%s\""

links = [
    "http://www.bay12games.com/dwarves/index.html",
    "http://www.bay12games.com/dwarves/older_versions.html"
]

print("Loading data from links...")
html = ""
for link in links:
    print ("Downloading %s: " % link, end="", flush=True)
    with urllib.request.urlopen(link) as response:
        html += str(response.read())
    print ("Done.")

print ("Parsing packs...")
packs_list = re.findall(
    '([\w]*.(zip|tar.bz2))', html)
print ("Found %d files." % len(packs_list))

if not packs_list:
    # I do not want error to be displayed here, but i want
    # give script information about something failing...
    print("Packs not found, aborting.")
    sys.exit(1)

counter = 0
number_of_packs = len(packs_list)
counters_space = len(str(number_of_packs))

print("Generating links list: ", end="", flush=True)
processed_packs = [
    {
        "name": pack[0],
        "link": link_template % pack[0],
        "format": pack[1],
    } for pack in packs_list
]
print("Done.")

print("Longest link is: ", end="", flush=True)
max_link_length = len(max(processed_packs, key=lambda x: len(x['link'])))
print(max_link_length)

for pack in processed_packs:
    counter += 1

    data_dict = {
        'link': pack['link'],
        'max_link_length': max_link_length,
        'counter': counter,
        'length': number_of_packs,
        'counters_space': counters_space,
        'progress': counter * 100.0 / number_of_packs
    }

    print(
        "Calling wget for \"{link:>{max_link_length}s}\" "
        "("
        "{counter:>{counters_space}d}"
        "/"
        "{length:>{counters_space}d}"
        ":"
        "{progress:>3.2f}%%"
        ")".format(**data_dict)
    )

    os.system(download_command % pack['link'])
