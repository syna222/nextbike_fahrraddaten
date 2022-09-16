import geopy
from geopy.geocoders import Nominatim
import os
import pandas as pd
import re
import reverse_geocoder as rg

## --- TAKES XML FILES (FOLDER) AND PUTS ALL PLACES AND ALL BIKES (PLUS THEIR PLACE-ID) INTO SEPARATE CSV FILES--- ##

def get_regex_matchlist(search_list, regex):      #every item from search_list is searched with regex + appended to super_list if it matches
    super_list = []
    for line in search_list:
        match = re.search(regex, line)
        if match:
            match = match.group(0)
            super_list.append(match)
    return super_list

def get_address(lat, lng):                        #gets address from coordinates (reverse geocoding)
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = lat + ", " + lng
    location = locator.reverse(coordinates)
    house_number = "X"                            #default house_number/postcode/street = "X" (non-existent), otherwise it's changed
    postcode = "X"
    street = "X"
    if "house_number" in location.raw["address"].keys():
        house_number = location.raw["address"]["house_number"]
    if "postcode" in location.raw["address"].keys():
        postcode = location.raw["address"]["postcode"]
    if "road" in location.raw["address"].keys():
        street = location.raw["address"]["road"]
    address = street + "/" + house_number + "/" + postcode
    return address


def my_main(file_data):
    #extract date/time from file + append to each entry later...:
    datetime_regex = "<datetime>(.*)</datetime>"
    datetime = re.search(datetime_regex, file_data).group(1)              #has to be in format "DD/MM/YY/hh:mm:ss"
    
    #open new csv-files:
    bikes_filename = os.path.join(r"C:\Users\vck\Documents\Python Scripts\bike_project\csvs_bikes", datetime.replace("/", ":").replace(":", "") + ".csv")
    places_filename = os.path.join(r"C:\Users\vck\Documents\Python Scripts\bike_project\csvs_places", datetime.replace("/", ":").replace(":", "") + ".csv")
    bikes_csv_file = open(bikes_filename, "w", encoding="utf-8")
    places_csv_file = open(places_filename, "w", encoding="utf-8")

    #get all place-elements with 1+ bike-elements from file + save to list:
    regex = "<place.+\n<bike.+\n(?:<bike.+\n)*</place>"                   #"(?: ...)" = non-capturing group
    match_list = re.findall(regex, file_data)
    
    #regex + dataframe for place entries:
    place_regex = "<place.+>"
    df_places = pd.DataFrame(columns=["uid", "lat", "lng", "address_string"])
    #regex + df for bike entries:
    bike_regex = "<bike.+/>"
    df_bikes = pd.DataFrame(columns=["number", "bike_type", "lock_types", "active", "state", "electric_lock", "boardcomp", "uid", "date_stamp"])
    #super_uid taken from each place-elem for all the included bikes:
    super_uid = ""

    for item in match_list:                                               #every item like "<place uid=...><bike number=.../><bike number=.../></place>"
        #print("ITEM:", item, "\n")
        line_list = item.split("\n")         
        place_linelist = get_regex_matchlist(line_list, place_regex)      #usually this should be only one match/place (but it uses same fct as bikes, so it's a list)
        #retrieve all data from place, save in df and use uid for bike:
        place_data_regex = "uid=\"(\d+)\" lat=\"(\d+\.\d+)\" lng=\"(\d+\.\d+)\""
        for line in place_linelist:
            line_match = re.search(place_data_regex, line)
            uid = line_match.group(1)                            
            super_uid = uid                                               #super_uid retrieval for use below in bike part
            lat = line_match.group(2)
            lng = line_match.group(3)
            #convert lat + lang:
            address = get_address(lat, lng)
            #append data as row to df_places:
            df_places = df_places.append({"uid":uid, "lat":lat, "lng":lng, "address_string":address}, ignore_index=True) #ignore_index, bc original index will change with adding dicts as rows to df
        #retrieve bike elements:
        bike_linelist = get_regex_matchlist(line_list, bike_regex)
        #retrieve all data from bike + save to df with super_uid from respective place:
        bike_data_reg = "number=\"(\d+)\" bike_type=\"(\d+)\" lock_types=\"(.*)\" active=\"(\d+)\" state=\"(.*)\" electric_lock=\"(\d+)\" boardcomputer=\"(\d+)\" pedelec_battery"
        for line in bike_linelist:
            line_match = re.search(bike_data_reg, line)
            number = line_match.group(1)
            bike_type = line_match.group(2)
            lock_types = line_match.group(3)
            active = line_match.group(4)
            state = line_match.group(5)
            electric_lock = line_match.group(6)
            boardcomp = line_match.group(7)
            #append data as row to df:
            df_bikes = df_bikes.append({"number":number, "bike_type":bike_type, "lock_types":lock_types, "active":active, "state":state, "electric_lock":electric_lock, "boardcomp":boardcomp, "uid":super_uid, "date_stamp":datetime}, ignore_index=True) #ignore_index, bc original index will not remain with adding dicts as rows to df

    #sort dfs:
    df_places.sort_values(by=["uid"], ascending=True, inplace=True)
    df_bikes.sort_values(by=["number"], ascending=True, inplace=True)
    #to csv:
    df_places.to_csv(places_csv_file, index=False, line_terminator="\n")
    places_csv_file.close()
    df_bikes.to_csv(bikes_csv_file, index=False, line_terminator="\n")
    bikes_csv_file.close()    
    
    
#MAIN CALL:
directory_xmls = r"C:\Users\vck\Documents\Python Scripts\bike_project\grabbed_xmls"
os.chdir(directory_xmls)
file_list = os.listdir(directory_xmls)
#do process for all xml files:
for name in file_list:
    file_path = os.path.join(directory_xmls, name)
    file = open(file_path, "r", encoding="utf-8")
    file_data = file.read()
    my_main(file_data)

    
    
    
    













