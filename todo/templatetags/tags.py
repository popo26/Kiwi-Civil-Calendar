import datetime

import geocoder
import requests
import os
from math import trunc
from django import template
import reverse_geocoder as rg
import pycountry
import netaddr


register = template.Library()

API_KEY=os.getenv("API_KEY")
# G_API_KEY=os.getenv("G_API_KEY")

ip_a = []

@register.simple_tag
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
        if len(ip_a):
            ip_a.clear()
            ip_a.append(ip)
        else:
            ip_a.append(ip)
        # print(f"ip_a1 insde is {ip_a[0]}")
    else:
        ip = request.META.get('REMOTE_ADDR')
        if len(ip_a):
            ip_a.clear()
            ip_a.append(ip)
        else:
            ip_a.append(ip)
        # print(f"ip_a2 outside is {ip_a[0]}")
    return ip



# Enable this function to find IP, Location etc data in base.html
# @register.simple_tag
# def get_location(request):
#     original_ip = ip()
#     # print(f"Original IP is {original_ip}")
#     #Because ip_address requires to be int
#     ip_address = ip2long(original_ip)
#     # print(f"ip_address is {ip_address}")

#     response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
#     location_data = {
#         "ip": ip_address,
#         "city": response.get("city"),
#         "region": response.get("region"),
#         "country": response.get("country_name")
#     }
#     # print(f"location data is {location_data}")
#     return location_data


#Convert IP string to Int
def ip2long(ip):
    return netaddr.IPAddress(ip)

def ip():
    if len(ip_a):
        ip = ip_a[0]
    else:
        #For local testing
        ip="8.8.8.8"
    return ip



def get_cordinates():
    client_ip = ip()
    g = geocoder.ip(client_ip)
    # print(f"g is {g}.")
    if IndexError:
        lat="-36.848461"
        lon="174.763336"
    else:
        lat=g.latlng[0]
        lon=g.latlng[1]
    
    cordinates = {
        "lat":lat,
        "lon":lon,
    }
    # print(f'cordinates is {cordinates}')
    return cordinates


def tuple_cordinates():
    cordinates = get_cordinates()
    lat = cordinates['lat']
    lon = cordinates['lon']
    return (lat, lon)
    

@register.simple_tag
def geo_name(request):
    original_ip = ip()
    ip_address = ip2long(original_ip)
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    city = response.get("city")
    return city

@register.simple_tag
def weather_api(request):
    cordinates = get_cordinates()
    lat = cordinates["lat"]
    lon = cordinates["lon"]
    weather_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_URL)
    data=response.json()
    current_weather = data["weather"][0]['description']
    return current_weather

@register.simple_tag
def temp_api(request):
    cordinates = get_cordinates()
    lat = cordinates["lat"]
    lon = cordinates["lon"]
    weather_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_URL)
    data=response.json()
    current_temp = trunc(data['main']["temp"])
    return current_temp

@register.simple_tag
def today(request):
    TODAY = datetime.date.today()
    nicer_format=TODAY.strftime('%a %d %b %Y')
    return nicer_format

@register.simple_tag
def time(request):
    now = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    return time


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    iso3166_1_alpha_2=result[0]['cc']
    pycountry_result = pycountry.countries.get(alpha_2=iso3166_1_alpha_2)
    return pycountry_result.name
    


