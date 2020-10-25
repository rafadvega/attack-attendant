import argparse
import prettytable
import csv
from pyattck import Attck
from prettytable import ALL as ALL


def output_screen(actors):
    table = prettytable.PrettyTable(hrules=prettytable.FRAME)
    table.field_names = ["Id", "Name"]
    for actor in actors:
        table.add_row([actor.id, actor.name])
    print(table)


def output_screen_verbose(actors):
    table = prettytable.PrettyTable(hrules=prettytable.ALL)
    table.field_names = ["Id", "Name", "Techniques"]
    for actor in actors:
        tech = ""
        for technique in actor.techniques:
            tech = tech + technique.id + " - " + technique.name + "\n"
        tech = tech[:-1]
        table.add_row([actor.id, actor.name, tech])
    print(table)


def check_detectable_actors(det, n):
    d = []
    nd = []
    attck = Attck()
    for actor in attck.enterprise.actors:
        actor_techniques = []
        for technique in actor.techniques:
            actor_techniques.append(technique.id[:5])
        common = list(set(det).intersection(actor_techniques))
        if len(common) > 0:
            d.append(actor)
        elif len(actor_techniques) > 0:
            nd.append(actor)
    if n:
        return(nd)
    else:
        return(d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true',
                        help='Output actor techniques')
    parser.add_argument('-n', action='store_true',
                        help='Output not detected actors instead detected actors')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-f', required=True,
                          help='file name with list of detectable techniques')

    args = parser.parse_args()

    with open(args.f) as f:
        detectables = f.read().splitlines()

    if args.v:
        output_screen_verbose(check_detectable_actors(detectables, args.n))
    else:
        output_screen(check_detectable_actors(detectables, args.n))


if __name__ == "__main__":
    main()
