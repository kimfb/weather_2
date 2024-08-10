import requests
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint


class MeteoData:

    __url = "https://api.open-meteo.com/v1/forecast"
    __geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, req):
        self.req = req
        self.location_data = None
        self.req_data = self.get_meteo_request()

    def set_location_data(self, req, lang='ru'):
        """Возвращает координаты запрашиваемого населённого пункта."""
        params = {
            'name': req,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        self.location_data = res['results']


    def get_coords(self):
        return self.location_data[0]['latitude'], self.location_data[0]['longitude']

    def get_hints(self, data, lang='ru'):
        """Возвращает список подсказок для строки ввода."""
        ans = dict()
        params = {
            'name': data,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        if res.get('results'):
            for val in res['results']:
                ans[val['name']] = val['country']
        return ans

    def get_meteo_request(self):
        """Получим ответ от open-meteo и переведём в pandas."""
        try:
            self.set_location_data(self.req)
        except LookupError:
            self.set_location_data('Москва')

        lat, lon = self.get_coords()

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

    def get_meteo_data(self):
        """Тестовая функция на замену трём вверху."""
        meteo = self.req_data
        cur = datetime.now()
        tom = datetime.now() + timedelta(days=1)
        res = dict.fromkeys(('current', 'today', 'tomorrow'))

        temp_meteo = meteo[(meteo['time'].dt.day == cur.day) & (meteo['time'].dt.hour == cur.hour)]
        res['current'] = {k: temp_meteo[k].values[0] if k != 'time' else temp_meteo[k] for k in temp_meteo}

        temp_meteo = meteo[(meteo['time'].dt.day == cur.day)]
        res['today'] = {k: temp_meteo[k].values if k != 'time' else temp_meteo[k] for k in temp_meteo}

        temp_meteo = meteo[(meteo['time'].dt.day == tom.day)]
        res['tomorrow'] = {k: temp_meteo[k].values if k != 'time' else temp_meteo[k] for k in temp_meteo}

        return res

    def get_location_data(self):
        """Возвращает название страны и населённого пункта для текущих координат"""
        return self.location_data[0].get('country'), self.location_data[0].get('name')


class MeteoOutput:

    @staticmethod
    def convert_temperature(temperature):
        """Коррекция вывода температуры."""
        if temperature > 0:
            return f'+{round(temperature)}'
        elif temperature < 0:
            return f'-{round(temperature)}'
        else:
            return 0

    @staticmethod
    def convert_cloud(cloudy):
        """Коррекция вывода облачности."""
        if cloudy < 10:
            return 'Ясно'
        elif cloudy < 40:
            return 'Малооблачно'
        elif cloudy < 70:
            return 'Переменная облачность'
        elif cloudy < 80:
            return 'Преимущественно облачно'
        else:
            return 'Пасмурно'

    @staticmethod
    def convert_preciption(rain, snowfall):
        """Коррекция вывода осадков."""
        if rain + snowfall < 1:
            return 'без осадков'
        elif snowfall > 1:
            if snowfall < 3:
                return 'небольшой дождь'
            elif snowfall < 15:
                return 'дождь'
            else:
                return 'сильный дождь'
        elif rain > 1:
            if rain < 3:
                return 'небольшой дождь'
            elif rain < 15:
                return 'дождь'
            elif rain >= 15:
                return 'сильный дождь'

    @staticmethod
    def convert_date(date):
        """Коррекция вывода даты."""
        weekday = ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
        month = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря')
        return f'{weekday[date.iloc[0].weekday()]}, {date.iloc[0].day} {month[date.iloc[0].month]}'
