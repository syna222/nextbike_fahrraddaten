from geopy.distance import geodesic
import sqlite3

## --- CALCULATES GEODISTANCE OVER PERIOD OF TIME (HERE: 1 WEEK) FOR EACH BIKE IN EXISTING DATABASE --- ##

conn = sqlite3.connect("next_bike.db")          #connects to existing database (has to be in same directory!)
c = conn.cursor()

def calc_singlebike_dist(bike_number, bike_dist_dict):
    #number of place instances for given bike:
    c.execute("SELECT COUNT(place_uid), bike_num FROM presence WHERE bike_num=" + bike_number +" GROUP BY bike_num")
    print(c.fetchall(), "\n")
    #number of distinct places for given bike:
    c.execute("SELECT COUNT(DISTINCT place_uid), bike_num FROM presence WHERE bike_num=" + bike_number +" GROUP BY bike_num")
    print(c.fetchall(), "\n")    
    #retrieves all available place instances for given bike w/ datestamp + geodata (chronologically!):
    c.execute("""SELECT DISTINCT place_uid, bike_num, date_stamp, lat, lng
                 FROM presence INNER JOIN places ON places.uid=presence.place_uid
                 WHERE bike_num=""" + bike_number)
    #make list of geodata-tuples (lat, lng) for bike:
    geotuple_list = []
    for row in c:
        #print(row, "\n")
        #get geodata + append to list:
        lat = row[3]
        lng = row[4]
        geo_tuple = (lat, lng)
        geotuple_list.append(geo_tuple)
    #calculate distance between all points in geotuple_list + get overall distance for bike for time period:
    distance_sum = 0
    prev_tup = geotuple_list[0] #set to first tuple
    #loop through all geodata points for bike and sum distances:
    for tup in geotuple_list:
        dist = geodesic(prev_tup, tup).kilometers
        distance_sum += dist
        prev_tup = tup
    #save bike_num + distance_sum as new pair to dictionary:
    new_pair = {bike_number:distance_sum}
    bike_dist_dict.update(new_pair)
    #return bike_dist_dict

def calc_dist_stats(bike_dist_dict):
    #max, min:
    max_bike = max(bike_dist_dict, key=bike_dist_dict.get)
    max_value = bike_dist_dict[max_bike]
    min_bike = min(bike_dist_dict, key=bike_dist_dict.get)
    min_value = bike_dist_dict[min_bike]
    #avg:
    distance_sum = 0
    for b in bike_dist_dict:
        dist = bike_dist_dict[b]
        distance_sum += dist
    avg_value = distance_sum / len(bike_dist_dict)
    #free + unused bikes:
    nullers = sum(val == 0 for val in bike_dist_dict.values())
    print("max distance:", max_value, "from bike number:", max_bike)
    print("min distance:", min_value, "from bike number:", min_bike)
    print("avg distance:", avg_value)
    print("number of unused bikes:", nullers)
    
    
    
    


##MAIN:
bike_dist_dict = {}                              #dictionary for adding each bike_num w/ its travelled distance via fct
#get all bike numbers + call function for each:
c.execute("SELECT DISTINCT number FROM bikes")   #save results! don't loop through cursor itself! method call will interfere...
bikenum_list = c.fetchall()
for bike in bikenum_list:
    bike_num = str(bike[0])
    if bike_num != "number":  #to exclude header from database!
        calc_singlebike_dist(bike_num, bike_dist_dict)
        
#save all bike numbers + their distances to file:
with open("bikesanddistances.txt", "w") as f:
    print(bike_dist_dict, file=f)

#calculate basic stats for bikes/dist:
with open("bikesanddistances.txt", "r") as f:
    calc_dist_stats(bike_dist_dict)






