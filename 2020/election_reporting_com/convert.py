#!/usr/bin/env python3

import re
import pandas as pd
import pdb
import argparse


def convert_to_csv(
    input_file_path='mi/kent/kent_county_president_cleaned.txt',
    output_file_path='mi/kent/kent_county_president_cleaned.csv'
):
    with open(input_file_path, 'r') as input_fp, open(output_file_path, 'w') as output_fp:
        counter = 0
        output_lines = []
        for line in input_fp.readlines():
            if counter == 0:
                header = [
                    l.strip(' ').rstrip('\n').replace(' ', '_') 
                    for l in line.lower()\
                        .replace('-', '_')\
                        .replace('/', '')\
                        .replace('.','')\
                        .split(',')
                ]
                print(f'header is {header}')
                # electionreporting.com specifc format
                # assuming first 4 columns always the same
                regex_string = (
                    r'(?P<{}>[\w\s]+Precinct \d+)\s+' #precint
                    r'(?P<{}>[\d]+)\s+' #registred voter
                    r'(?P<{}>[\d]+)\s+' #ballot case
                    r'(?P<{}>[\d.\%]+)\s+' # turnout
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                    # r'(?P<{}>[\d]+)\s+'
                ).format(
                    *header[0:4]
                ) + ''.join(
                    [r'(?P<{}>[\d]+)\s+'.format(h) for h in header[4:]]
                )
                output_line = ','.join(header)
                output_lines.append(output_line)
                
                counter += 1
                continue

            new_line = line.replace(',', '')
            new_line = new_line.replace('%', '')
            ret = re.match(regex_string, new_line)
            if ret is None:
                print(f'line does not match regex: \n{new_line}')
                print('press c to continue or q to quit')
                pdb.set_trace()
                continue

            output_line = ','.join(
                ret[x] for x in header
            )
            output_lines.append(output_line)
            
        output_fp.writelines('\n'.join(output_lines))
    return output_file_path

def main():
    parser = argparse.ArgumentParser(description='convertion to csv file')
    parser.add_argument(
        'input_file_path', 
        type=str, 
        default='mi/kent/kent_county_president_cleaned.txt'
    )
    parser.add_argument(
        'output_file_path', 
        type=str, 
        default='mi/kent/kent_county_president_cleaned.csv'
    )
    args = parser.parse_args()
    output_file_path = convert_to_csv(
        args.input_file_path,
        args.output_file_path
    )
    print(f'csv file generated {output_file_path}')
    df = pd.read_csv(output_file_path, header=0)



            

def test_regex(regex_string, input_string, list_of_fields):
    ret = re.match(regex_string, input_string)
    for f in list_of_fields:
        print(ret[f])
    return ret
    
def test_run():
    regex_string = (
        r'(?P<precinct>[a-zA-Z\s]+)'
        r'(?P<registred_voters>[\d]+)\s+'
        r'(?P<ballots_cast>[\d]+)\s+'
        r'(?P<turnout>[\d.\%]+)\s+'
        r'(?P<biden>[\d.\%]+)\s+'
        r'(?P<trump>[\d]+)\s+'
        r'(?P<jorgensen>[\d]+)\s+'
        r'(?P<blankenship>[\d]+)\s+'
        r'(?P<hawkins>[\d]+)\s+'
        r'(?P<fuente>[\d]+)\s+'
        r'(?P<total_write_in>[\d]+)\s+'
    )
    input_string = "Ada Township Precinct 1 1,316 1,090 82.83% 589 472 13 1 0 0 0"
    list_of_fields = ['precinct', 'registred_voters', 'turnout', 'biden', 'trump']
    test_regex(regex_string, input_string, list_of_fields)

if __name__ == '__main__':
    main()
    