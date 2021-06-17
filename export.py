import datetime
import os
import pandas as pd 

def export_to_pub(df, name_export):
    """
    This function exports a dataframe as an excel spreadsheet, and includes a data-dictionary 
    param: a dataframe, and a string that'll be the name of the file
    return: None
    """
    
    # Get general information
    timestamp = datetime.datetime.now()
    no_rows = df.shape[0]
    no_cols = df.shape[1]
    # Build dictionary to export
    meta_data = pd.DataFrame({'Compiled last' : [timestamp],
                              'Number of rows' : [no_rows],
                              'Number of columns' : [no_cols]})
    
    # Build column list and loop through them to build table of variables
    keys_list = df.columns.to_list()
    
    list_dicts = []

    for i, key in enumerate(keys_list):
        dict_key = {}
        dict_key['Column name'] = key
        dict_key['Type'] = df[key].dtype
        dict_key['Number of missing values'] = df[key].isna().sum()
        dict_key['Description variable'] = input("What does column '%s' represent?"%key)
        dict_key['Source variable'] = input("Link to source?")
        dict_key['Manually calculated?'] = input("Were calculations done by me? (Y/N)")
        print("Completed for %d out of %d variable"%(i+1, len(keys_list)))
        list_dicts.append(dict_key)
        
    data_dict = pd.DataFrame(list_dicts)
    
    # Export as excel spreadsheet in output folder
    cwd = os.getcwd()
    if os.path.isdir('output'): 
        pass
    else:
        os.mkdir('output')
    path_export = cwd + "/output/"        
        
    with pd.ExcelWriter('%s%s.xlsx'%(path_export, name_export)) as writer:  
        df.to_excel(writer, sheet_name='data')
        meta_data.to_excel(writer, sheet_name = 'dictionary', index = False)
        data_dict.to_excel(writer, sheet_name='dictionary', index = False, startrow = 3)
    
    print("Finished export, find the file in output folder.")
    
    return None