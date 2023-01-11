import atmosphere as atm
import re

month_names = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"Ju\
ne",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

def DateTime(date_time_str):
    """Returns the date and time string into separate formatted string"""
    
    time_str = ""
    date_strng = ""

    cmd = date_time_str         
    pattern_time = r'\s[(\d+)]+'         # Pattern for extracting time
    result = re.search(pattern_time,cmd)
    hour = int(result[0])
    if hour >=0 and hour <= 12:
        if hour == 0:
            time_str += "12 PM in the night"
        else:
            time_str += "{} AM in the morning".format(hour)
    elif hour>12 and hour <= 17:
        time_str += "{} PM in the afternoon".format((hour)-12)
    elif hour>17 and hour <=20:
        time_str+= "{} PM in the evening".format((hour)-12)
    elif hour>20 and hour <=23:
        time_str+= "{} PM in the night".format((hour)-12)


    date_str = cmd[:result.start()]
    pattern_date = r'([(\d+)]+)-([(\d+)]+)-([(\d+)]+)'      # Pattern for extracting date
    result_date = re.search(pattern_date,date_str)
    month_num = int(result_date[2])
    date_strng += "{} {} {}".format(result_date[3],month_names[month_num],result_date[1])
    
    return date_strng,time_str

def WeatherForecast(place):
    """Returns the min and max temperature, and weather of next day"""
    
    lst = atm.showForecast(place,9)
    clouds_dict = {}
    max_temp = 0
    date_max = ''

    min_temp = 40
    date_min = ''

    for entries in lst:
        if entries[1] < min_temp:
            date_min,min_temp,clouds_min = entries
            
        if entries[1] > max_temp:
            date_max,max_temp,clouds_max = entries

        if entries[2] not in clouds_dict:
            clouds_dict[entries[2]] = 1
        else:
            clouds_dict[entries[2]] +=1

    sky_rating = sorted(clouds_dict)
    mindate_str,mintime_str = DateTime(date_min)
    maxdate_str,maxtime_str = DateTime(date_max)
    
    return_str = "Weather forecast for tomorrow is.. \nThe minimum \
temperature will be {mintemp:.2f} degree celsius at {mintime} on {mindate}.. and \nThe maximum \
temperature will be {maxtemp:.2f} degree celsius at {maxtime} on {maxdate}.. \nTomorrow there \
will be {sky}".format(mintemp=min_temp,mintime=mintime_str,mindate=mindate_str,maxtemp=max_temp,maxtime=maxtime_str,maxdate=maxdate_str,sky=sky_rating[0])
    return return_str

def Weather5Days(place):
    """Return the weather forecast for 5 days"""
    lst = atm.showForecast(place,40)
    for entries in lst:
        datetime_str,temp,clouds  = entries
        date,time = DateTime(datetime_str)
        print("{}: {:.2f} C\t{} at [{}]".format(date,temp,clouds,time))
        print("----------------------------------------------------")
