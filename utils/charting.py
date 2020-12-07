import pandas as pd
#import seaborn as sns
from matplotlib import pyplot as plt
import pdb
import glob

def get_all_dataframe(
    data_source='election_reporting_dot_com',
    state='mi',
    year=2020,
):
    county_folder_list = [
        x.split('/')[-2] for x in glob.glob(
            './election_reporting_com/2020/mi/*/'
        )
    ]
    state = 'mi'

    df_dict_all = {
        'party': pd.DataFrame(),
        'president': pd.DataFrame(),
        'senator': pd.DataFrame()
    }
    for county in county_folder_list:
        print(f'getting dataframe for county {county}')
        df_dict = get_county_dataframe(
            data_source='election_reporting_dot_com', 
            state='mi', 
            county=county, 
            year=2020
        )
        # pdb.set_trace()
        for x in df_dict.keys():
            if x in df_dict_all:
                df_dict_all[x] = pd.concat(
                    [df_dict_all[x], df_dict[x]],
                    ignore_index=True
                )
            else:
                print(f'key {x} not recognized. precess c to continue')
                pdb.set_trace()

    return df_dict_all

    


def get_county_dataframe(
    data_source='election_reporting_dot_com', 
    state='mi', 
    county='kent', 
    year=2020
):
    '''
    get data pandas dataframe dictionary given state, conuty, year and data source
    '''
    if data_source == 'election_reporting_dot_com':
        file_list = glob.glob(
            f'./election_reporting_com/{year}/{state}/{county}/*cleaned.csv'
        )
        df_dict = {}
        # df_dict_keys = [
        #     x.split('/')[-1].split('.')[0] for x in file_list
        # ]
        df_dict_keys = ['party', 'president', 'senator']

        # for x, y in zip(df_dict_keys, file_list):
        for y in file_list:
            print(f'reading from {y}')
            for x in df_dict_keys:
                if x in y:
                    df_dict[x] = pd.read_csv(y)
    else:
        return None

    return df_dict


def plot_president_vs_senator_all_counties(
    fig_counter_base=100, 
    state='mi',
    save_figure=True,
    year=2020
):
    fig_counter = fig_counter_base
    
    df_dict = get_all_dataframe()
    
    df_p = df_dict['president']
    df_s = df_dict['senator']
    # precincts = df_p['precinct'].unique()
    df_merge = pd.merge(df_p, df_s, suffixes=('_p', '_s'), how='inner', on='precinct')
    senator_dem_key = None
    senator_rep_key = None
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

    if senator_dem_key is None or senator_rep_key is None:
        print(f'data for county {county} has column that does not have expected key')
        pdb.set_trace()
        

    total_president_series = df_merge[biden_key] + df_merge[trump_key]
    df_president_percentage_dem = df_merge[biden_key]/total_president_series
    df_president_percentage_rep = df_merge[trump_key]/total_president_series

    df_diff_dem = df_merge[biden_key]/total_president_series - df_merge[senator_dem_key]
    df_diff_rep = df_merge[trump_key]/total_president_series - df_merge[senator_rep_key]

    total_senator_series = df_merge[senator_dem_key]+df_merge[senator_rep_key]
    df_senator_percentage_dem = df_merge[senator_dem_key]/total_senator_series
    df_senator_percentage_rep = df_merge[senator_rep_key]/total_senator_series

    pdb.set_trace()
    fig_counter += 1
    plt.figure(fig_counter)
    party = 'republican'
    title = f'{party} {state} all avaiable counties'
    plt.title(title)
    # plt.scatter(df_senator_percentage_rep, df_diff_rep)
    plt.scatter(df_senator_percentage_rep, df_president_percentage_rep)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    if save_figure:
        filename = 'pdfs/electioncom/'+title.replace(' ', '_')+'.pdf'
        plt.savefig(filename)
        print(f'saving figure {filename}')
    else:
        plt.draw()
        plt.pause(0.001)

    fig_counter += 1
    plt.figure(fig_counter)
    party = 'democrats'
    title = f'{party} {state} all avaiable counties'
    plt.title(title)
    # plt.scatter(df_senator_percentage_dem, df_diff_dem)
    plt.scatter(df_senator_percentage_dem, df_president_percentage_dem)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    if save_figure:
        filename = 'pdfs/electioncom/'+title.replace(' ', '_')+'.pdf'
        print(f'saving figure {filename}')
        plt.savefig(filename)
    else:
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")


def plot_president_vs_senator_per_county(
    county, 
    fig_counter_base, 
    state='mi',
    save_figure=True,
    year=2020
):
    fig_counter = fig_counter_base
    # file_list = glob.glob(
    #     f'./election_reporting_com/{year}/{state}/{county}/*cleaned.csv'
    # )
    
    # df_dict = {}
    # df_dict_keys = [
    #     x.split('/')[-1].split('.')[0] for x in file_list
    # ]

    # for x, y in zip(df_dict_keys, file_list):
    #     print(f'reading from {y}, dict key: {x}')
    #     df_dict[x] = pd.read_csv(y)
    #     if 'party' in y:
    #         df_sp = df_dict[x]
    #     elif 'president' in y:
    #         df_p = df_dict[x]
    #     elif 'senator' in y:
    #         df_s = df_dict[x]
    #     else:
    #         print(f'unknown file {y} with key being {x}')
    df_dict = get_county_dataframe(county=county,year=year,state=state)
    df_p = df_dict['president']
    df_s = df_dict['senator']
    # precincts = df_p['precinct'].unique()
    # df_merge = pd.merge(df_p, df_s, suffixes=('_p', '_s'))
    df_merge = pd.merge(df_p, df_s, suffixes=('_p', '_s'), how='inner', on='precinct')
    senator_dem_key = None
    senator_rep_key = None
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
    # for x in df_sp.columns:
    #     if 'democratic_party' in x:
    #         sp_dem_key = x
    #     elif 'republican_party' in x:
    #         sp_reb_key = x

    if senator_dem_key is None or senator_rep_key is None:
        print(f'data for county {county} has column that does not have expected key')
        pdb.set_trace()
        

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
    title = f'{party} {state} {county}'
    plt.title(title)
    # plt.scatter(df_senator_percentage_rep, df_diff_rep)
    plt.scatter(df_senator_percentage_rep, df_president_percentage_rep)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    if save_figure:
        filename = 'pdfs/electioncom/'+title.replace(' ', '_')+'.pdf'
        plt.savefig(filename)
        print(f'saving figure {filename}')
    else:
        plt.draw()
        plt.pause(0.001)

    fig_counter += 1
    plt.figure(fig_counter)
    party = 'democrats'
    title = f'{party} {state} {county}'
    plt.title(title)
    # plt.scatter(df_senator_percentage_dem, df_diff_dem)
    plt.scatter(df_senator_percentage_dem, df_president_percentage_dem)
    plt.xlabel(f'senator votes fractions for {party}')
    plt.ylabel(f'president votes fractions for {party}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    if save_figure:
        filename = 'pdfs/electioncom/'+title.replace(' ', '_')+'.pdf'
        print(f'saving figure {filename}')
        plt.savefig(filename)
    else:
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")
