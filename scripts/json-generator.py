# attack_layers_simple.py - the "hello, world" for ATT&CK Navigator layer generation
# Takes a simple CSV file containing ATT&CK technique IDs and counts of groups, software and articles/reports that reference this technique
# and generates an ATT&CK Navigator layer file with techniques scored and color-coded based on an algorithm
# This sample is intended to demonstrate generating layers from external data sources such as CSV files.

import argparse
import csv
import json
import sys

# Static ATT&CK Navigator layer JSON fields
LAYER_VERSION = "4.0"
NAV_VERSION = "4.0"
NAME = "Attck Detection Coverage"
DESCRIPTION = "Attck Detection Coverage"
DOMAIN = "enterprise-attack"

# Main
def main():

    # handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", action="store", dest="input",
                        required=True, help="input ATT&CK csv file with tactic ID, groups, software, etc... fields")
    parser.add_argument("-o", "--ouput", action="store", dest="output",
                        required=True, help="output Navigator layer json file")

    args = parser.parse_args()

    # Base ATT&CK Navigator layer
    layer_json = {
        "versions": {
            "layer": LAYER_VERSION,
            "navigator": NAV_VERSION
        },
        "name": NAME,
        "description": DESCRIPTION,
        "domain": DOMAIN,
        "techniques": []
    }

    # parse csv file, calculating a score for each technique and adding that to the layer
    with open(args.input, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            # score each technique based on a simple formula
            if row["Coverage"] == "NA":
                score = 0
                color = "#bdbdbd"
            else:
                score = int(float(row["Coverage"])*100)
                color = ""
            technique = {
                "techniqueID": row["ID"],
                "score": score,
                "color": color
            }

            layer_json["techniques"].append(technique)


    # add a color gradient (white -> red) to layer
    # ranging from zero (white) to the maximum score in the file (red)
    layer_json["gradient"] = {
        "colors": [
            "#ffffff",
			"#ffb067",
			"#fbfb47",
			"#8ec843"
        ],
        "minValue": 0,
        "maxValue": 100
    }

    # output JSON
    with open(args.output, 'w') as f:
        json.dump(layer_json, f, indent=4)


if __name__ == "__main__":
    main()