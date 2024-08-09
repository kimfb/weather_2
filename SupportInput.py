

def input_temperature(temperature):
    '''Коррекция вывода температуры.'''
    if temperature > 0:
        return f'+{round(temperature)}'
    elif temperature < 0:
        return f'-{round(temperature)}'
    else:
        return 0

def output_cloudy(cloudy):
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


def output_precipitation(rain, snowfall):
    if rain+snowfall < 1:
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

def output_date(date):
    weekday = ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
    month = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
             'сентября', 'октября', 'ноября', 'декабря')
    return f'{weekday[date.iloc[0].weekday()]}, {date.iloc[0].day} {month[date.iloc[0].month]}'








