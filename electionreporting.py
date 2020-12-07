#!/usr/bin/env python

import glob
import pdb
from utils.charting import plot_president_vs_senator_per_county, plot_president_vs_senator_all_counties

def main():
    county_folder_list = glob.glob(
        './election_reporting_com/2020/mi/*/'
    )
    print('plotting per county data')
    state_abbreviation = 'mi'
    fig_counter_base = 100
    for county_folder in county_folder_list:
        county = county_folder.split('/')[-2]
        plot_president_vs_senator_per_county(
            county, 
            fig_counter_base, 
            state_abbreviation,
            save_figure=True
        )
        fig_counter_base += 100

    print('plotting aggregated data')
    plot_president_vs_senator_all_counties()

def plot_all():
    plot_president_vs_senator_all_counties()

if __name__=='__main__':
    main()

