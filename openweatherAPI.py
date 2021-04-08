import urllib.request
import json


def getOutsideCondition(apikey, cityId):
    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric&lang=pl'.format(cityId, apikey)
    forecastUrl = 'http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric&lang=en&cnt=10'.format(cityId, apikey)

    http = urllib.request.urlopen(url)
    jsonString = http.read()
    weatherInfo = json.loads(jsonString)

    http = urllib.request.urlopen(forecastUrl)
    jsonString = http.read()
    forecast = json.loads(jsonString)

    return {"current" : weatherInfo, "forecast" : forecast}