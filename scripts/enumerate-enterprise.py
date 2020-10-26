import argparse
import sys
import prettytable
import csv
from pyattck import Attck
from prettytable import ALL as ALL

attack = Attck()


def output_screen(dic):
    table = prettytable.PrettyTable(hrules=prettytable.FRAME)
    table.field_names = ["Id", "Name"]
    for key in dic:
        table.add_row([key, dic[key]])
    print(table)
    print("TOTAL: " + str(len(dic)))


def output_csv(dic, file_name):
    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames = ['Id', 'Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for key in dic:
            writer.writerow({'Id': key, 'Name': dic[key]})


def list_techniques():
    d = {}
    for technique in attack.enterprise.techniques:
        d[technique.id] = technique.name
    return(d)


def list_malware():
    d = {}
    for malware in attack.enterprise.malwares:
        d[malware.id] = malware.name
    return(d)


def list_tactics():
    d = {}
    for tactic in attack.enterprise.tactics:
        d[tactic.id] = tactic.name
    return(d)


def list_tools():
    d = {}
    for tool in attack.enterprise.tools:
        d[tool.id] = tool.name
    return(d)


def list_actors():
    d = {}
    for actor in attack.enterprise.actors:
        d[actor.id] = actor.name
    return(d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', action='store_true',
                        help='Output CSV instead output screen')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--list', choices=['techniques', 'malwares', 'tactics', 'tools',
                                             'actors'], required=True, help='list techniques, malwares, tactics, tools or actors')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list == "techniques":
        d = list_techniques()
    elif args.list == "malwares":
        d = list_malware()
    elif args.list == "tactics":
        d = list_tactics()
    elif args.list == "tools":
        d = list_tools()
    elif args.list == "actors":
        d = list_actors()

    if args.csv:
        output_csv(d, args.list+".csv")
    else:
        output_screen(d)


if __name__ == "__main__":
    main()
