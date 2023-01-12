import datetime as dt
import requests as rqst
import re
from geopy.geocoders import ArcGIS

nom = ArcGIS()
weatherApiKey = ''              # Put your API Key here

def showTemp(place):
        """Returns a tuple of clouds, temperature and feels like temp in degree celsius"""
        
        addrs,latlng = nom.geocode(place)
        url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latlng[0],latlng[1],weatherApiKey)
        weather = rqst.get(url).json()
        clouds_list = weather['weather']
        clouds = (clouds_list[0])['description']    #Clouds details
        mainweather = weather['main']   
        temp,feels_like = (mainweather['temp']-273.15), (mainweather['feels_like']-273.15)     # Temperature details
        return clouds,temp,feels_like


def showForecast(place,limit):
        """Returns a list of tuples of timestamps, temperature, clouds in Kelvin"""
        
        forecast_list = []
        addrs,latlng = nom.geocode(place)
        url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(latlng[0],latlng[1],weatherApiKey)
        fcast = (rqst.get(url).json())['list']
        nextday = fcast[0:limit]            # Forecast for next day
        for fields in nextday:
                main_dict = fields['main']
                temp_k = (main_dict['temp']-273.15)
                tup = (fields['dt_txt'], temp_k,((fields['weather'])[0])['description'])       #Tuple of results
                forecast_list.append(tup)
        return forecast_list


def showAirQuality(place):
        """Returns a tuple of Air quality index and components"""
        
        cmpdict = {}
        result = ""
        addrs,latlng = nom.geocode(place)
        url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'.format(latlng[0],latlng[1],weatherApiKey)     
        air_qlty = ((rqst.get(url).json())['list'])[0]          
        index = (air_qlty['main'])['aqi']
        if(index == 1):
                result = "Good"
        elif index == 2:
                result = "Fair"
        elif index == 3:
                result = "Moderate"
        elif index == 4:
                result = "Poor"
        elif index == 5:
                result = "Very poor"
        comps = (air_qlty['components'])
        for key,vals in comps.items():
                cmpdict[key] = vals*0.001
        return index,result,cmpdict

        
