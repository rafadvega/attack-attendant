from attackcti import attack_client
import json, sys, argparse, traceback, csv
from itertools import zip_longest
from collections import defaultdict
import prettytable
import argparse


def output_screen(dic):
    table = prettytable.PrettyTable(hrules=prettytable.FRAME)
    table.field_names = ["Id", "Name"]
    for key in dic:
        table.add_row([key, dic[key]])
    print(table.get_string(sortby="Id"))
    print("TOTAL: " + str(len(dic)))


def output_csv(dic, file_name):
    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames = ['Id', 'Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for key in dic:
            writer.writerow({'Id': key, 'Name': dic[key]})


def get_tactics():
    client = attack_client()
    enterprise_tactics = client.get_enterprise_tactics()
    tactics={}
    for tactic in enterprise_tactics:
        tactics[(tactic['external_references'][0])['external_id']] = tactic['name']
    return tactics


def get_techniques(platform):
    client = attack_client()
    enterprise_techniques = client.get_enterprise_techniques()
    techniques={}
    for technique in enterprise_techniques:
        try:
            revoked = technique['revoked']
        except:
            revoked = False
        try:
            subt = technique['x_mitre_is_subtechnique']
        except:
            subt = False
        if (revoked is False) and (subt is False) and ("This technique has been deprecated" not in technique['description'] ):
            if (len(platform) == 0) or (len(set([i.lower() for i in technique['x_mitre_platforms']]) & set(platform)) > 0):
                techniques[(technique['external_references'][0])['external_id']] = technique['name']
    return techniques


def get_matrix(filename, platform):
    client = attack_client()
    enterprise_techniques = client.get_enterprise_techniques()
    tactics = defaultdict(list)
    for technique in enterprise_techniques:        
        try:
            revoked = technique['revoked']
        except:
            revoked = False
        try:
            subt = technique['x_mitre_is_subtechnique']
        except:
            subt = False
        if (revoked is False) and (subt is False) and ("This technique has been deprecated" not in technique['description'] ):
            if (len(platform) == 0) or (len(set([i.lower() for i in technique['x_mitre_platforms']]) & set(platform)) > 0):
                for tactic in technique['kill_chain_phases']:
                    tactics[tactic['phase_name']].append(technique['name'])
    matrix = []
    for tactic in tactics:
        matrix.append(tactics[tactic])
    with open(filename, 'w', encoding="ISO-8859-1", newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerows([list(tactics.keys())])
        writer.writerows(zip_longest(*matrix, fillvalue = ''))
    myfile.close()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", action="store", dest="platform", default=[],
                        help='Filter by platform in techniques and matrix. Example: -p windows linux macOS network')
    parser.add_argument('-o', action="store", dest="output", default="",
                        help='Output csv file name')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-s', dest="select", choices=['tactics', 'techniques', 'matrix'], required=True)
    args = parser.parse_args()

    platform = [i.lower() for i in args.platform]

    if args.select == "tactics":
        if args.output != "":
            output_csv(get_tactics(), args.output)
        else:
            output_screen(get_tactics())
    elif args.select == "techniques":
        if args.output != "":
            output_csv(get_techniques(platform), args.output)
        else:
            output_screen(get_techniques(platform))
    elif args.select == "matrix":
        if args.output != "":
            get_matrix(args.output, platform)
        else:
            print("To get matrix, use -o argument")   

if __name__ == "__main__":
    main()