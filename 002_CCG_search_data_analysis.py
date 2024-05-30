

############# 0 - Setup

## Load packages
import pandas as pd
import os 

pd.set_option('display.max_columns', None)


encodings = ['utf-8', 'latin-1', 'utf-16']


## Declare paths
path_input = "/Users/Juliette/Dropbox/Documents/References/CCG_Search/"
path_output = "/Users/Juliette/Dropbox/Documents/References/CCG_Search/Output/"
output_name = "Unique_Entries_"


############# I - Data procession

######## Creating the list of the synonyms for all the various items:
# Synonyms for developing countries (emerging economies, LMICs, economies in transition, etc.)
# But also creating verticals for each main region
list_dvc = ["developing countries", "emerging economies", "economies in transition", "low and middle income countries", "LMICs", "global south"] 

list_areas = ["Africa", "South East Asia", "BRICs", "ASEAN"]

list_regions = list_dvc + list_areas

######## Creating the list of the various policy verticals, and each specific policy (so pricing --> subsidies, carbon tax, ETS...)
list_policy_vertical = {"pricing":['subsidies', 'carbon tax', 'emissions trading schemes', 'emissions trading scheme', 'ETS'], "finance":["finance","investment", "investments"], "regulation":["standards","energy efficiency", "energy markets"], "skills":["just transition", "training"]}

dict_synonyms = {"ETS": ["emissions trading schemes", "emissions trading scheme", "ETS"] , "investment":["investment", "investments"]}

list_paths = []


def create_dataframe_summary_stats(my_dict, list_regions):
    ### I want the df to look like this:
        ##  Region | Subtitle 
    titles_list = my_dict.keys()
    data_df_base = {"Region":[],"Subtitle":[],"Nb Rows":[]}
    df = pd.DataFrame(data_df_base)
    for title in titles_list:
        for policy in my_dict[title]:
            for region in list_regions:
                data = {"Region": [region], "Subtitle": [policy], "Nb Rows": [""]}
                df_1 = pd.DataFrame(data)
                print(df_1)
                df = pd.concat([df,df_1])
                print(df)#df.append({"Region": region, "Subtitle": policy, "Nb Rows": ""}, ignore_index=True)
    # df = df.iloc[3:, 1:]
    # df = df.reset_index(drop=True)
    return df

df_summary_statistics = create_dataframe_summary_stats(list_policy_vertical,list_regions)



#### Create a dictionary of all the files. It looks like this:
    ### dict {subsidies [query_1, query_2, query_3], carbon tax [query_1, query_2] } etc. 
def produce_list_path(my_dict):
    dict_of_dataframes = {}
    for policy in my_dict.keys():
        for subtitle in my_dict[policy]:
            list_of_dataframes_names = []
            path = path_input + policy + "/" + subtitle.replace(" ","_") 
            for file_name in sorted(os.listdir(path)):
                list_of_dataframes_names.append(path + "/" + file_name)
            dict_of_dataframes[subtitle]= list_of_dataframes_names
    return dict_of_dataframes

dict_of_dataframes_per_region = produce_list_path(list_policy_vertical)


### Count the number of rows in the files. 
def count_number_of_rows(my_dict, df_output):
    for policy_vertical in my_dict.keys():
        print(f"Policy vertical {policy_vertical}")
        for subtitle in my_dict[policy_vertical]: 
            print(f"subtitle {subtitle}")
            for region in list_regions:
                print(f"region is {region}")
                file = path_input + "/" + policy_vertical + "/" + subtitle.replace(" ","_") + "/" + "001_query_" + region.replace(" ","_") + ".csv"
                if os.path.getsize(file) == 0:
                    df_output.loc[(df_output["Region"] == region) & (df_output["Subtitle"] == subtitle), "Nb Rows"] = 0
                else:
                    p = pd.read_csv(file)
                    df_output.loc[(df_output["Region"] == region) & (df_output["Subtitle"] == subtitle), "Nb Rows"] = p.shape[0]
    return df_output

df_summary_statistics = count_number_of_rows(list_policy_vertical, df_summary_statistics)


### Get the final CSV files combining all the searches with the synonyms, but:
    ### Keep only unique values (we drop entries with the same title and same author)
    ### Filter by dropping the elements that had less than 50 cites in the years before 2022
def produce_unique_rows(dict_of_dataframes,output_name):
    dict_df_unique = {}
    for subtitle in dict_of_dataframes.keys():
        i = 0
        for p in dict_of_dataframes[subtitle]:
            print(p)
            if os.path.getsize(p) > 0:
                if i == 0:
                    df = pd.read_csv(p, encoding = 'utf-8')
                else:
                    df_1 = pd.read_csv(p, encoding = 'utf-8')
                    df = pd.concat([df, df_1])#df.append(df_1)
                i = i+1
        df = df[df["Year"] != "Year"]
        df['Year'] = df["Year"].fillna(0)
        df["Year"] = pd.to_numeric(df["Year"], errors = "coerce")
        df['Year'] = df['Year'].astype("Int64")
        df["Cites"].fillna(0)
        df["Cites"] = pd.to_numeric(df["Cites"], errors = "coerce")
        df["Cites"] = df["Cites"].astype("Int64")
        df.sort_values(by = 'Cites', ascending = False)
        df = df.drop_duplicates(subset = ['Title','Authors'], keep = 'first')
        ### Create the 'Check' variable
        df['To_Drop'] = 0  # Initialize all values to 0
        df.loc[(df['Cites'] < 50) & (df['Year'] < 2022), 'To_Drop'] = 1
        ### Keep only the variable To Drop = 0 
        df = df[df.To_Drop == 0]
        dict_df_unique[subtitle] = df
        df.to_csv(path_output + "002_" + output_name + subtitle.replace(" ","_") + ".csv")
    return dict_df_unique

produce_unique_rows(dict_of_dataframes_per_region, output_name)

