import requests
import pandas as pd
from datetime import datetime, timedelta


class MeteoData:
    """
    Класс для работы с метеорологическими данными с использованием API Open Meteo.

    Атрибуты класса:
         __url (str): URL API для получения метеорологических данных.
        __geo_url (str): URL API для геокодирования (поиска географического расположения).

     Атрибуты экземпляров:
        __req (str): Запрос, переданный пользователем.
        __location_data (dict): Данные о текущей локации.
        __req_data (dict): Метеорологические данные текущей локации.

    Методы:
         update_req:
            Обновить запрос. Основная функция для обновления данных экземпляра класса.
         get_location_data:
            Получение название населенного пункта и страны для текущей локации.
        __set_location_data:
            Меняет информацию о текущей локации, отправляет запрос к __geo_url. Вызывается методом get_meteo_request.
        get_meteo_request:
            Отправляет запрос по адресу __url, возвращает метео-данные. Вызывается при инициализации или update_req.
        get_coords:
            Возвращает текущие координаты.
        get_hints:
            Формирует словарь подсказок для пользователя при вводе. Отправляет запрос __geo_url.
        get_meteo_data:
            Возвращает словарь с подготовленными метеоданными для current, today и tomorrow.
    """

    __url = "https://api.open-meteo.com/v1/forecast"
    __geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, req):
        self.__req = req
        self.__location_data = None
        self.__req_data = self.get_meteo_request()

    def update_req(self, value):
        """Обновить запрос. Основная функция для обновления данных экземпляра класса."""
        self.__req = value
        self.__req_data = self.get_meteo_request()

    def get_location_data(self):
        """Возвращает название страны и населённого пункта для текущих координат"""
        return self.__location_data.get('country'), self.__location_data.get('name')

    def __set_location_data(self, req, lang='ru'):
        """Записывает данные (dict) о запрашиваемой локации в self.location_data."""
        req = req[:req.find(',')] if req.count(',') else req
        params = {
            'name': req,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        self.__location_data = res['results'][0]

    def get_meteo_request(self):
        """Получим ответ от open-meteo в формате DataFrame."""
        try:
            self.__set_location_data(self.__req)
        except LookupError:
            self.__set_location_data('Москва')

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

    def get_coords(self):
        """Возвращает координаты (tuple) текущей локации."""
        return self.__location_data['latitude'], self.__location_data['longitude']

    def get_hints(self, data, lang='ru'):
        """Возвращает подсказки для строки ввода.

        Args:
            data: текст запроса (str)
            lang: язык результата запроса (str)
        Returns:
            A dict.
        """

        params = {
            'name': data,
            'language': lang
        }
        res = requests.get(self.__geo_url, params=params).json()
        if res.get('results'):
            ans = {val['name']: val['country'] if val.get('country') else val['name']
                   for val in res['results']}
            return ans

        return dict()

    def get_meteo_data(self):
        """Получить подготовленные данные о погоде.

        Returns:
            A dict. Словарь с тремя ключам: 'current', 'today', 'tomorrow'.
        """

        meteo = self.__req_data
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


class MeteoOutput:
    """
    Класс для форматирования и преобразования метеорологических данных в удобочитаемый вид.

    Методы:
        convert_temperature(temperature):
            Преобразует температуру в формат с указанием знака (+ или -) и округлением до целого числа.
        convert_cloud(cloudy):
            Преобразует значение облачности в текстовое описание состояния неба.
        convert_preciption(rain, snowfall):
            Преобразует значения дождя и снега в текстовое описание интенсивности осадков.
        convert_date(date):
            Преобразует дату в формат, включающий день недели и месяц.
    """

    @staticmethod
    def convert_temperature(temperature):
        """Пользовательский вид для температуры."""
        if temperature > 0:
            return f'+{round(temperature)}'
        elif temperature < 0:
            return f'-{round(temperature)}'
        else:
            return 0

    @staticmethod
    def convert_cloud(cloudy):
        """Пользовательский вид для облачности."""
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
        """Пользовательский вид для вывода осадков."""
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
        """Пользовательский вид для вывода даты."""
        weekday = ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
        month = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря')
        return f'{weekday[date.iloc[0].weekday()]}, {date.iloc[0].day} {month[date.iloc[0].month]}'
