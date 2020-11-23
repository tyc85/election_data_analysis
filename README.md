# election_data_analysis

## Data from electionreportin.com
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
    
    

## Data from Openelections
