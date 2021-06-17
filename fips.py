import addfips 
import pandas as pd 
import numpy as np

# only glob 
mapping_places = pd.read_csv('https://raw.githubusercontent.com/mariepastora/open_data/main/census_geocoded_2018.csv')
mapping_places = mapping_places.astype({"State Code (FIPS)": str, 
            "County Code (FIPS)": str,
            "Place Code (FIPS)" : str,
            "Consolidtated City Code (FIPS)" : str})

mapping_places = mapping_places[['State Code (FIPS)', 'County Code (FIPS)',
                                'Place Code (FIPS)', 'Consolidtated City Code (FIPS)',
                                "Area Name (including legal/statistical area description)"]]
mapping_places.columns = ['state_fips', 'county_fips', 'place_fips', 'consolidated_fips', 'name']

# appropriate zfills
mapping_places['state_fips'] = mapping_places['state_fips'].apply(lambda x: x.zfill(2))
mapping_places['county_fips'] = mapping_places['county_fips'].apply(lambda x: x.zfill(3))
mapping_places['place_fips'] = mapping_places['place_fips'].apply(lambda x: x.zfill(5))

def add_state_fips_as_col(col_state, vint):
    """
    This function has to be applied directly on the dataframe 
    You can use via df.apply(lambda x: add_state_fips_as_col(x['state_col'], 2015), axis = 1)
    param: state col, a vintage (year, either 2000, 2010, 2015)
    return: a state fips code
    """
    val_state = col_state
    if val_state == "Washington, D.C.":
        return 11
    elif val_state == "Washington DC":
        return 11
    elif val_state == "Washington, DC":
        return 11
    elif val_state == "District of Columbia":
        return 11
    elif val_state == "Washington, District of Columbia":
        return 11
    elif val_state == "DC":
        return 11
    elif val_state == "D.C.":
        return 11 
    elif val_state == "Guam":
        return 66
    elif val_state == "GU":
        return 66
    elif val_state == "Virgin Islands":
        return 78
    elif val_state == "VI":
        return 78
    elif val_state == "Northern Mariana Islands":
        return 69
    elif val_state == "MP":
        return 69
    elif val_state == "Puerto Rico":
        return 72
    elif val_state == "PR":
        return 72
    else:
        af = addfips.AddFIPS(vintage = vint)
        state = val_state
        fip = af.get_state_fips(state)

        return fip

def add_county_fips_as_col(col_county, col_state, vint):
    val_state = col_state
    val_county = col_county
    
    af = addfips.AddFIPS(vintage = vint)
    fip = af.get_county_fips(val_county, val_state)

    return fip


def get_fips_place(col_city, col_state_fips):
    """
    Based on a city name returns a FIPS code for the place. 
    Let's be honest, this is kind of sketch so be careful when using
    will work if the city name does not have "city" in it 
    Then you'll need to join on index with original dataframe
    Also this is slow

    param: columns of city and fips of state
    return: a pandas series

    """

    # city name should have CITY added except for new york 
    city = str(col_city).rstrip().lstrip().title() 
    
    if city == "New York City":
        city = "New York city"
    else:
        city += " city"

    state = str(col_state_fips)
     
    # fix metro gov of Nashville
    if (city == 'Nashville city' and state == '47'):
        city = "Nashville-Davidson metropolitan government (balance)"

    try: 
        # filter for the correct thing
        redux = mapping_places[(mapping_places['state_fips'] == state) &
                      (mapping_places['name'] == city ) & 
                               (mapping_places['place_fips'] != "00000") ]

        # and then take the first return value so that's the super sketch part

        s = pd.Series({"census_state_fips" : redux['state_fips'].iloc[0],
        "census_county_fips" : redux['county_fips'].iloc[0],
        "census_place_fips" : redux['place_fips'].iloc[0],
        "census_name" : redux['name'].iloc[0],
        "deduced_from_no_cities": redux.shape[0]})

    except:
        s = pd.Series({"census_state_fips" : state,
        "census_county_fips" : np.nan,
        "census_place_fips" : np.nan,
        "census_name" : city,
        "deduced_from_no_cities": np.nan})
    
    return s

