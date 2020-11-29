import pandas as pd
#import seaborn as sns
from matplotlib import pyplot as plt
import pdb
import glob

def plot_president_vs_senator_per_county(
    county, 
    fig_counter_base, 
    state_abbreviation='mi',
    save_figure=True
):
    fig_counter = fig_counter_base
    file_list = glob.glob(
        f'./election_reporting_com/2020/{state_abbreviation}/{county}/*cleaned.csv'
    )
    
    df_dict = {}
    df_dict_keys = [
        x.split('/')[-1].split('.')[0] for x in file_list
    ]

    for x, y in zip(df_dict_keys, file_list):
        print(f'reading from {y}, dict key: {x}')
        df_dict[x] = pd.read_csv(y)
        if 'party' in y:
            df_sp = df_dict[x]
        elif 'president' in y:
            df_p = df_dict[x]
        elif 'senator' in y:
            df_s = df_dict[x]
            
    # precincts = df_p['precinct'].unique()
    df_merge = pd.merge(df_p, df_s, suffixes=('_p', '_s'))
    for x in df_p.columns:
        if 'biden' in x:
            biden_key = x
        elif 'trump' in x:
            trump_key = x
    for x in df_s.columns:
        if '_dem' in x:
            senator_dem_key = x
        elif '_rep' in x:
            senator_rep_key = x
    for x in df_sp.columns:
        if 'democratic_party' in x:
            sp_dem_key = x
        elif 'republican_party' in x:
            sp_reb_key = x

    total_president_series = df_merge[biden_key] + df_merge[trump_key]
    df_president_percentage_dem = df_merge[biden_key]/total_president_series
    df_president_percentage_rep = df_merge[trump_key]/total_president_series

    df_diff_dem = df_merge[biden_key]/total_president_series - df_merge[senator_dem_key]
    df_diff_rep = df_merge[trump_key]/total_president_series - df_merge[senator_rep_key]

    total_senator_series = df_merge[senator_dem_key]+df_merge[senator_rep_key]
    df_senator_percentage_dem = df_merge[senator_dem_key]/total_senator_series
    df_senator_percentage_rep = df_merge[senator_rep_key]/total_senator_series

    fig_counter += 1
    plt.figure(fig_counter)
    party = 'republican'
    title = f'{party} {state_abbreviation} {county}'
    plt.title(title)
    # plt.scatter(df_senator_percentage_rep, df_diff_rep)
    plt.scatter(df_senator_percentage_rep, df_president_percentage_rep)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    if save_figure:
        filename = 'pdfs/'+title.replace(' ', '_')+'.pdf'
        plt.savefig(filename)
        print(f'saving figure {filename}')
    else:
        plt.draw()
        plt.pause(0.001)

    fig_counter += 1
    plt.figure(fig_counter)
    party = 'democrats'
    title = f'{party} {state_abbreviation} {county}'
    plt.title(title)
    # plt.scatter(df_senator_percentage_dem, df_diff_dem)
    plt.scatter(df_senator_percentage_dem, df_president_percentage_dem)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    if save_figure:
        filename = 'pdfs/'+title.replace(' ', '_')+'.pdf'
        print(f'saving figure {filename}')
        plt.savefig(filename)
    else:
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")
