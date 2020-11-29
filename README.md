# election_data_analysis
## Quickstart
### General
- make sure you have python 3.6+ 
- run setup.sh, which will setup a virtualenv in python named election_analysis in home folder and activates it
- run ./electionreporting.py in terminal to generate pdf figures in the folder pdfs/ for avaialble counties 
- can also start jupyter notebook by typeing ```jupyter notebook``` in terminal and open the notebook electioncom_2020.ipynb and execute the cell
- to access openelctions.com data as submodule:
    - git submodule init
    - git submodule update


## Data from electionreporting.com
Since 2020 election data is not widely available yet, we used unofficial source to obtain preliminary data. Michigan unofficial data is obtained from https://electionreporting.com/
### Adding new data
Steps to add more data and use the included conversion script to produce csv data:
1. go to https://electionreporting.com/
2. select any county/city that's not in the repo already
3. scroll down to look for "cards" of different eleciton, most importantly the following three cards 
    - Straight Party
    - President/Vice-President
    - United States Senator
4. for each card, click the vertical ... button to open results per precinct
5. copy the entire table down and save it as a .txt file according to the naming convention, e.g., if we are getting straight party table's data for city of Detroit:
    - save as name city_of_detroit_straight_party.txt in the folder mi/city_of_detroit/
    - for presidential, use the name city_of_detroit_president.txt, and for senator, use city_of_detroit_senator.txt
6. clean the data as follows and save the new file as :
    - replace all tabs with space using your favorite editor's function in one shot
    - remove the second line (total aggregation, we don't need this)
    - replace the string "TOTALS: X of Y" in the first line with Precinct
    - add a comma as delimiter for the first line, which is to be used as header/columns for pandas dataframe
    - save the new file as city_of_detroit_straight_party_cleaned.txt, using straight party data as example
    
    
### Analysis Methodology

#### Presidents vs. Senator 
- for each precinct, compute the fraction voted for democratic and the republican presidential candidate
- for each precinct, compute the fraction voted for democratic and the republican senator candidte
- for each county, plot a scatter plot where X-axis is fractions voted for party A's senator candidate, and Y-axis is fractions voted for party A's presidential candidate

#### Presidents vs. Straight Party 
- Stright party votes is interesting but only available in certain states, e.g., Michigan

## Data from Openelections
