#!/usr/bin/env python

import pandas as pd
import numpy as np
import pdb
import seaborn as sns
from matplotlib import pyplot as plt
import pdb


states_df = pd.read_csv('./states_abbreviations.csv')
# for state, state_abbreviation in zip(states_df['State'], states_df['Abbreviation']):
#     print(f'state is {state}')
#     print(f'state_abbreviation is {state_abbreviation}')
    

def gather_votes_per_precinct(df):
    dem_diff = []
    rep_diff = []
    dem_house = []
    rep_house = []
    rep_house_percent_list = []
    dem_house_percent_list = []
    dem_president_percentage_list = []
    rep_president_percentage_list = []
    precincts = df['precinct'].unique()
    for precinct in precincts:
        if precinct == '9999':
            # need to investigate this precinct, strange
            continue

        try:
            df_per_precinct = df[
                (df['precinct'] == precinct)
            ]

            rep_president_votes = df_per_precinct[
                (df_per_precinct['party'] == 'REP')
                & 
                (df_per_precinct['office'] == 'President')
            ]['votes'].values[0]

            dem_president_votes = df_per_precinct[
                (df_per_precinct['party'] == 'DEM')
                & 
                (df_per_precinct['office'] == 'President')
            ]['votes'].values[0]

            rep_house_vote_list = df_per_precinct[
                (df_per_precinct['office'] != 'President') & (df_per_precinct['party'] == 'REP')
            ]['votes'].tolist()
            dem_house_vote_list = df_per_precinct[
                (df_per_precinct['office'] != 'President') & (df_per_precinct['party'] == 'DEM')
            ]['votes'].tolist()
        except IndexError as e:
            print(f'error {str(e)}\n{df_per_precinct}')

        
        if len(rep_house_vote_list) == 0 or len(dem_house_vote_list) == 0:
            print(f'no house votes in precinct {precinct}:\n{df_per_precinct}')
            print('skipping the entry')
            continue


        rep_house_votes = sum(rep_house_vote_list)/len(rep_house_vote_list)
        dem_house_votes = sum(dem_house_vote_list)/len(dem_house_vote_list)
        dem_house.append(dem_house_votes)
        rep_house.append(rep_house_votes)
        if rep_house_votes + dem_house_votes == 0:
            rep_house_percent = 0
            dem_house_percent = 0
            print(f'precinct {precinct} got zero party vote on both sides')
        else:
            total_house_votes = (dem_house_votes+rep_house_votes)
            rep_house_percent = float(rep_house_votes)/total_house_votes
            dem_house_percent = float(dem_house_votes)/total_house_votes


        rep_house_percent_list.append(rep_house_percent)
        dem_house_percent_list.append(dem_house_percent)
        total_president_votes = dem_president_votes + rep_president_votes
        if total_president_votes == 0:
            print(f'precinct {precinct} got zero presidential vote on both sides')
            dem_president_percentage = 0
            rep_president_percentage = 0
        else:
            dem_president_percentage = float(dem_president_votes)/total_president_votes
            rep_president_percentage = float(rep_president_votes)/total_president_votes
            
        dem_diff.append(dem_president_votes - dem_house_votes)
        rep_diff.append(rep_president_votes - rep_house_votes)

        dem_president_percentage_list.append(dem_president_percentage)
        rep_president_percentage_list.append(rep_president_percentage)


    data = {
        'rep_diff': rep_diff, 
        'dem_diff': dem_diff,
        'rep_house': rep_house, 
        'dem_house': dem_house,
        'rep_house_percent': rep_house_percent_list,
        'dem_house_percent': dem_house_percent_list,
        'rep_president_percent': rep_president_percentage_list,
        'dem_president_percent': dem_president_percentage_list,
    }
    # df_scatter = pd.DataFrame(data=d)

    return data

def get_scatter_df(
    state_abbreviation, 
    csv_file_path='./openelections-data-mi/2016/20161108__mi__general__precinct.csv'
):
    state = state_abbreviation.lower()
    print(f'processing {state}')
    df = pd.read_csv(csv_file_path)
    
    # Problem: precinct does not sync up
    # df_president_rep = df[
    #     (df['party'] == 'REP')
    #     & 
    #     (df['office']=='President')
    # ]['votes'].reset_index(drop=True)
    # df_president_dem = df[
    #     (df['party'] == 'DEM')
    #     & 
    #     (df['office']=='President')
    # ]['votes'].reset_index(drop=True)
    # df_president_total = df_president_rep + df_president_dem

    # df_house_rep = df[
    #     (df['office'] == 'U.S. House') & (df['party'] == 'REP')
    # ]['votes'].reset_index(drop=True)
    # df_house_dem = df[
    #     (df['office'] == 'U.S. House') & (df['party'] == 'DEM')
    # ]['votes'].reset_index(drop=True)
    # df_house_total = df_house_rep + df_house_dem

    data = gather_votes_per_precinct(df)
    # pdb.set_trace()
    # Need to align precincts
    
    return data

def main():
    # states_df = pd.read_csv('./states_abbreviations.csv')
    fig_counter = 1
    # year = 2016
    csv_file_path_dict = {
        'mi_2016': './openelections/openelections-data-mi/2016/20161108__mi__general__precinct.csv',
        # 'pa_2016': './openelections/openelections-data-pa/2016/20161108__pa__general__precinct.csv',
        'mi_2012': './openelections/openelections-data-mi/2012/20121106__mi__general__precinct.csv',
    }
    # state_name, state_abbreviation in zip(states_df['State'], states_df['Abbreviation'])
    save_figure = True
    for state_abbreviation in csv_file_path_dict:
        df_scatter = get_scatter_df(
            state_abbreviation, 
            csv_file_path_dict[state_abbreviation]
        )
        for party in ['rep', 'dem']:
            plt.figure(fig_counter)
            plt.xlabel(f'senator votes fractions for {party}')
            plt.ylabel(f'president votes fractions for {party}')
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            title = f'{party} {state_abbreviation}'
            plt.title(title)
            plt.scatter(
                df_scatter[f'{party}_house_percent'], 
                df_scatter[f'{party}_president_percent'],
                marker='o'
            )
            if save_figure:
                filename = 'pdfs/openelections/'+title.replace(' ', '_')+'.pdf'
                print(f'saving figure {filename}')
                plt.savefig(filename)
            else:
                plt.draw()
                plt.pause(0.001)
                input("Press [enter] to continue.")
            fig_counter +=1



if __name__=='__main__':
    main()