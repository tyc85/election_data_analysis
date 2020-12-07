#!/usr/bin/env python3

import re
import pandas as pd
import pdb
import argparse
import glob


def clean_txt_file(
    input_file_path='./election_reporting_com/2020/mi/saginaw/saginaw_county_president.txt', 
    output_file_path='./election_reporting_com/2020/mi/saginaw/saginaw_county_president_cleaned.csv'
):
    '''
    only clean up the tabs. still need to manually create comma separate headers
    '''
    counter = 0
    with open(input_file_path, 'r') as input_fp, open(output_file_path, 'w') as output_fp:
        for line in input_fp.readlines():
            # second line always total tally and needs to be removed
            counter += 1
            if 'TOTAL\t' in line or 'TOTAL ' in line:
                continue
            
            new_line = line.replace('\t', ' ')
            output_fp.write(new_line)

            
    return output_file_path

def convert_to_csv(input_file_path, output_file_path):
    '''
    convert cleaned txt file copied from election.com table to csv file
    refer to README.md in root folder to contribute to "cleaned" data
    '''
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
                    r'(?P<{}>[\w.\s]+(Precinct|AVCB)[\s\d\w]*)\s+' #precint
                    r'(?P<{}>[\d]+)\s+' #registred voter
                    r'(?P<{}>[\d]+)\s+' #ballot case
                    r'(?P<{}>[\d.\%]+)\s+' # turnout
                ).format(
                    *header[0:4]
                ) + ''.join(
                    [r'(?P<{}>[\d]+)\s+'.format(h) for h in header[4:]]
                )

                output_line = ','.join(header)
                output_lines.append(output_line)
                
                counter += 1
                continue

            if '(Out of County)' in line:
                print(f'skipping entry with (Out of County)\n: {line}')
                continue
            
            # replace comma and percentage
            new_line = line.replace(',', '').rstrip('\n')
            new_line = new_line.replace('%', '')
            ret = re.match(regex_string, new_line)
            if ret is None:
                print(
                    f'in file {input_file_path} line does not match regex {regex_string}: '
                    f'\n{new_line}'
                )

                split_line = new_line.split(' ')
                output_line = ','.join(
                    [' '.join(split_line[0:len(split_line) - len(header) + 1]),]
                    + split_line[-len(header)+1:]
                )
                print('attempting a different match using header length:')
                print(output_line)
                # print('press c to accept this match and continue or q to quit')
                # pdb.set_trace()
            else:
                output_line = ','.join(
                    ret[x] for x in header
                )
            output_lines.append(output_line)
            
        output_fp.writelines('\n'.join(output_lines))
    return output_file_path

def main():
    parser = argparse.ArgumentParser(description='convertion to csv file')
    parser.add_argument(
        '-i',
        dest='input_file_path', 
        type=str, 
        default='mi/kent/kent_county_president_cleaned.txt'
    )
    parser.add_argument(
        '-o',
        dest='output_file_path', 
        type=str, 
        default='mi/kent/kent_county_president_cleaned.csv'
    )
    parser.add_argument(
        '-d',
        dest='source_dir', 
        type=str, 
        default=None
    )
    args = parser.parse_args()
    output_file_path_list = []
    if args.source_dir is None:
        input_file_path = args.input_file_path
        output_file_path = args.output_file_path
        output_file_path_list.append(convert_to_csv(
            input_file_path,
            output_file_path
        ))
    else:
        output_file_path_list = convert_pipline(args.source_dir)

    return output_file_path_list

    

def convert_pipline(source_dir):
    cleaned_txt_file_list = glob.glob(source_dir.rstrip('/')+'/*cleaned.txt')
    output_file_path_list = []
    print(f'convering files in directory {source_dir}, file list {cleaned_txt_file_list}')
    for f in cleaned_txt_file_list:
        input_file_path = f
        output_file_path = f.replace('.txt', '.csv')
        print(
            f'converting {input_file_path} to {output_file_path}'
        )
        convert_to_csv(input_file_path, output_file_path)
        output_file_path_list.append(output_file_path)

    return output_file_path_list


if __name__ == '__main__':
    main()
    
