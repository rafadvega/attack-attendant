import argparse
import prettytable
import csv
from pyattck import Attck
from prettytable import ALL as ALL


def output_all(attck):
    subtechniques = int()
    tec_sub = int()
    platforms = []
    datasources = []
    for technique in attck.enterprise.techniques:
        subtechniques += len(technique.subtechniques)
        if technique.platforms is not None:
            platforms += technique.platforms
        if technique.data_source is not None:
            datasources += technique.data_source
        if len(technique.subtechniques) == 0:
            tec_sub += 1
        else:
            tec_sub += len(technique.subtechniques)

    table = prettytable.PrettyTable(hrules=prettytable.ALL)
    table.field_names = ["CATEGORY", "COUNTS"]
    table.add_row(["Tactics", len(attck.enterprise.tactics)])
    table.add_row(["Techniques", len(attck.enterprise.techniques)])
    table.add_row(["Subtechniques", subtechniques])
    table.add_row(["Techniques/Subtechniques", tec_sub])
    table.add_row(["Platforms", len(set(platforms))])
    table.add_row(["Datasources", len(set(datasources))])
    table.padding_width = 10
    print(table)


def output_by_platform(attck):
    platforms = []
    for technique in attck.enterprise.techniques:
        if technique.platforms is not None:
            platforms += technique.platforms
    platforms_dict = {i: platforms.count(i) for i in set(platforms)}
    table = prettytable.PrettyTable(hrules=prettytable.ALL)
    table.field_names = ["Platform", "Techniques Count", "Percent %"]
    total_tech = len(attck.enterprise.techniques)
    for i in platforms_dict:
        table.add_row([i, platforms_dict[i], str(round(
            (platforms_dict[i]/total_tech)*100, 2))])
    print(table)


def main():

    attck = Attck()
    output_all(attck)
    output_by_platform(attck)


if __name__ == "__main__":
    main()
