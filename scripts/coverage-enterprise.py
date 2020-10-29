from attackcti import attack_client
import json, sys, argparse, traceback, csv
from itertools import zip_longest
from collections import defaultdict
import prettytable
import argparse
import statistics


def get_matrix_coverage(coverage, platform):
    client = attack_client()
    enterprise_techniques = client.get_enterprise_techniques()
    tactics = defaultdict(list)
    no_coverage = ""
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
                    try:
                        tactics[tactic['phase_name']].append(coverage[(technique['external_references'][0])['external_id']])
                    except KeyError:
                        tactics[tactic['phase_name']].append("0")
                        no_coverage += (tactic['phase_name'] + ": " + technique['name'] + "\n")
    if no_coverage != "":
        print("--------------------------------")
        print("TÉCNICAS NO PRESENTES EN EL CSV:")
        print("--------------------------------")
        print(no_coverage)
        print("* se considera cobertura 0 en las mismas")
        print("--------------------------------")
    return tactics
    


def import_coverage(filename):
    coverage={}
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        for row in csv_reader:
            if first == True:
                first = False
            else:
                coverage[row[0]] = row[1]
    return coverage


def coverage_calculation(tactics):
    tactics_average = {}
    total = 0
    table_totals = prettytable.PrettyTable(hrules=prettytable.ALL)
    table_tactics = prettytable.PrettyTable(hrules=prettytable.ALL)
    for tactic in tactics:
        tactic_cov = []
        for technique in tactics[tactic]:
            if technique != "NA":
                tactic_cov.append(int(float(technique)*100))
        tactics_average[tactic] = round(statistics.mean(tactic_cov),2)
    for tactic in tactics_average:
        total += tactics_average[tactic]
    matrix_tact_avrg = round(total/len(tactics_average),2)

    # Print
    table_totals.title = 'ATT&CK Coverage'
    table_totals.field_names = ["Concept", "Value"]
    table_tactics.title = 'Tactics Coverage'
    table_tactics.field_names = ["Concept", "Value"]
    table_totals.add_row(["Matrix Coverage by Tactic", matrix_tact_avrg])
    for key in tactics_average:
        table_tactics.add_row([key, tactics_average[key]])
    print("\n\n")
    print(table_totals)
    print("\n\n")
    print(table_tactics)


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", action="store", dest="platform", default=[],
                        help='Filter by platform in techniques and matrix. Example: -p windows linux macOS network')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', action="store", dest="input", default="", required=True,
                        help='Input csv file name. Format: id,score')
    args = parser.parse_args()

    platform = [i.lower() for i in args.platform]

    #get CSV coverage
    coverage = import_coverage(args.input)

    #Correlate coverage with matrix
    tactics = get_matrix_coverage(coverage, platform)

    #Calculate Average
    coverage_calculation(tactics)

if __name__ == "__main__":
    main()