import requests
import pandas as pd
from dadata import Dadata
from datetime import datetime, timedelta

class MeteoData:

    __url = "https://api.open-meteo.com/v1/forecast"
    __geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, req):
        self.req = req
        self.location_data = None
        self.req_data = self.get_meteo_request()

    def get_coords(self, location, lang='ru'):
        ''' Получаем координаты запрашиваемого населённого пункта.'''
        params = {
            'name': self.req,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        self.location_data = res['results']

        return res['results'][0]['latitude'], res['results'][0]['longitude']

    def get_hints(self, data, lang='ru'):
        params = {
            'name': data,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        return False if not res.get('results') else res['results']

    def get_meteo_request(self):
        '''Получим ответ от open-meteo и переведём в pandas.'''
        try:
            lat, lon = self.get_coords(self.req)
        except:
            lat, lon = self.get_coords('Москва')
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m",
                       "apparent_temperature",
                       "cloud_cover",
                       "rain",
                       "showers",
                       "snowfall",
                       'wind_speed_10m',
                       "pressure_msl",
                       "relative_humidity_2m"]
        }
        res = requests.get(self.__url, params=params).json()
        res = pd.DataFrame(res['hourly'])
        # Все даты в формат timestamp, для удобства поиска по времени
        res['time'] = pd.to_datetime(res['time'])
        return res

    # def get_current_meteo(self):
    #     meteo = self.get_meteo_request()
    #     cur = datetime.now()
    #     current_meteo = meteo[(meteo['time'].dt.day == cur.day) & (meteo['time'].dt.hour == cur.hour)]
    #     current_meteo = {k: current_meteo[k].values[0] for k in current_meteo}
    #     return current_meteo
    #
    # def get_today_meteo(self):
    #     meteo = self.get_meteo_request()
    #     cur = datetime.now()
    #     today_meteo = meteo[(meteo['time'].dt.day == cur.day)]
    #     # Всё в словарь, дату оставляем в том же формате
    #     today_meteo = {k: today_meteo[k].values if k != 'time' else today_meteo[k] for k in today_meteo}
    #     return today_meteo
    #
    # def get_tomorrow_meteo(self):
    #     meteo = self.get_meteo_request()
    #     tom = datetime.now() + timedelta(days=1)
    #     tomorow_meteo = meteo[(meteo['time'].dt.day == tom.day)]
    #     tomorow_meteo = {k: tomorow_meteo[k].values if k != 'time' else tomorow_meteo[k] for k in tomorow_meteo}
    #     return tomorow_meteo

    def get_meteo_data(self, req_time='current'):
        '''Тестовая функция на замену трём вверху'''
        meteo = self.req_data
        cur = datetime.now()
        tom = datetime.now() + timedelta(days=1)
        if req_time == 'today':
            res_meteo = meteo[(meteo['time'].dt.day == cur.day)]
            res_meteo = {k: res_meteo[k].values if k != 'time' else res_meteo[k] for k in res_meteo}
        elif req_time == 'tomorrow':
            res_meteo = meteo[(meteo['time'].dt.day == tom.day)]
            res_meteo = {k: res_meteo[k].values if k != 'time' else res_meteo[k] for k in res_meteo}
        else:
            res_meteo = meteo[(meteo['time'].dt.day == cur.day) & (meteo['time'].dt.hour == cur.hour)]
            res_meteo = {k: res_meteo[k].values[0] for k in res_meteo}

        return res_meteo

    def get_location_data(self):
        return self.location_data[0].get('country'), self.location_data[0].get('name')



