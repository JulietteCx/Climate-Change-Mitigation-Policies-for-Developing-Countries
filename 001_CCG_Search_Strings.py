########### Automation of the search strategy

############# # Description of the code
# This code takes the search strategy described in the methodology section of the paper to create search strings and performs an automated search using google scholar. 
# For each type of policy (each subsection in the paper, such as subsidies, carbon pricing, energy regulation, etc.) it creates all the queries following this format: 
# keyword, as discussed will be "climate change mitigation" + developing country (or a synonym, see "list_dev_countries", or a region, see "list_regions")   + policy vertical (see list_policy_vertical) 
# year restricted to 2010 - 2023
# title contains the word in the subsection titles (see list_subsection)
# for instance, the query pop8query --gscholar --keywords "climate policy mitigation emerging economies regulation" --years 2010-2023 --title "energy markets" --max 100 --format csv >> /Users/Juliette2/Dropbox/Documents/References/regulation/energy_markets/001_query1.csv
# looks at papers with the relevant keywords  (climate policy mitigation emerging economies regulation) in the text, whose title contains "energy markets". 
# it then stores the results in a separate dataset. 
# I restrict to a maximum number of 100 results. 
# Need to download the Publish & Perish software and the Publish or Perish command line tool 


######## Outputs: 
# in the path_output specified below, this code will create four different folders (one for each policy vertical) and four different subfolders (one for each policy type, such as subsidies). It will then store the results of all the queries. 
# 001_Queries_list.txt --> list of all the queries ran
# All the results of the literature search. (> regulation > energy_markets > 001_query1.csv for instance)

############ Replicability may be impacted by your operating device, whether you have the application Publish or Perish as well as its command line packaging & the location of the results file from the query ran in the terminal. 
### By recaptcha and by spaces in your output directory 
### Remove the spaces in the output folder.
### Note that it might be that you cannot run all the queries at the same time.  



########## Structure of the code:
# 0 - Setup : Packages, declare variables and the inputs
# I - Automating the queries based on the various synonyms. 
#		1) Creating the dictionary that will contain all the final queries
# 		2) Create the list of all the possible queries
#		3) Now run the query in terminal and create all the relevant files
#		4) Create the list of queries in a separate text file.


################################################################
#               0 - Setup                                      #
# Loading various packages and setting up the output directory #
################################################################


###### Packages and paths

import os

## Path for your output 
######### !-! Change here the output for replicability !-!
path_output = "/Users/Juliette/Dropbox/Documents/References/CCG_Search/"

if not os.path.exists(path_output):
    os.makedirs(path_output)





######## Creating the list of the synonyms for all the various items:
# Synonyms for developing countries (emerging economies, LMICs, economies in transition, etc.)
# But also creating verticals for each main region

list_dvc = ["developing countries"]#, "emerging economies", "economies in transition", "low and middle income countries", "LMICs", "global south"] 

list_areas = []#["Africa", "South East Asia", "BRICs", "ASEAN", "China"]

list_regions = list_dvc + list_areas

######## Creating the list of the various policy verticals, and each specific policy (so pricing --> subsidies, carbon tax, ETS...)
# Dictionary policy vertical: policy section in key, and all the subsections in values. 
list_policy_vertical =  {"pricing":['subsidies']}
                         #, 'carbon tax', 'emissions trading schemes', 'emissions trading scheme', 'ETS'], "finance":["finance", "investment", "investments"], "regulation":["standards", "energy efficiency", "energy markets"], "skills":["just transition", "training"]}


#### Drop >50 for years < 2022
#### keep papers >= 2022 


################################################################
#               I - Automating the queries                     #
#             Based on the various synonyms                    #
################################################################


### 1) Creating the dictionary that will contain all the final queries, for each sub-policy type. The dictionary will look like:
# {pricing:['subsidies', 'carbon taxes'], regulation:['energy markets', 'standards']}
dict_queries ={}

#### 2) Create the list of all the possible queries
for section in list_policy_vertical.items():
    for subsection in range (0,len(section[1])):
        dict_queries[section[1][subsection]] = []
        subfile_name = section[1][subsection].replace(" ","_")
        path_file = str(path_output) + str(section[0]) +"/" + str(subfile_name) 
        if not os.path.exists(path_file):
                os.makedirs(path_file)
        k = 0
        for region in list_regions:
            path_export = path_file + "/001_query_" + region.replace(" ","_") + ".csv"
            #### The query must have the following """ at the beginning. then around the script, it must have "{script}". If within the script there are " we need to replace by \\"
            query = """pop8query --gscholar --keywords \\\" climate policy mitigation """ + region + " " + section[0] + " " +"""\\\" """ + "--years 2010-2023 --title \\\"" + str(section[1][subsection]) + "\\\" --max 100 --format csv " + ">> " + str(path_export) 
            k = k+1
            dict_queries[section[1][subsection]].append(query)



queries_list = "" 
####### 3) Now run the query in terminal and create all the relevant files
for key in dict_queries.keys():
    for query in dict_queries[key]:
        queries_list = queries_list + "\n" + query
        print(f"query {query}")
        command = """osascript -e 'tell application "Terminal" to do script "{}" '""".format(query.replace("'", "'\\''"))
        print(command)
        os.system(command)
 
####### 4) Create the list of queries in a separate text file.

with open(path_output + '001_Queries_List.txt', 'w') as f:
    f.write(queries_list)


