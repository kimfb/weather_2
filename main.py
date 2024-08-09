from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from SupportInput import input_temperature, output_cloudy, output_precipitation, output_date
from MeteoData import MeteoData

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>ggfd689(dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)

meteo = MeteoData('Москва')

# Добавление функций для использования их в шаблонах
app.jinja_env.globals.update(input_temperature=input_temperature,
                             output_cloudy=output_cloudy,
                             output_precipitation=output_precipitation,
                             output_date=output_date)
# # app.jinja_env.filters['input_temperature'] = input_temperature

@app.route('/', methods=['POST', 'GET'])
def index():
    global meteo
    words=()
    if request.is_json:
        data = request.get_json()
        if data.get('type'):
            words = data['data']
    elif request.form:
        print(request.headers)
        meteo = MeteoData(request.form['location'])

    cur_meteo = meteo.get_meteo_data('current')
    tod_meteo = meteo.get_meteo_data('today')
    tom_meteo = meteo.get_meteo_data('tomorrow')

    return render_template('index.html', cur_meteo=cur_meteo,
                                         tod_meteo=tod_meteo,
                                         tom_meteo=tom_meteo,
                                         hints=meteo.get_hints(words),
                                         loc=meteo.get_location_data())




if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=4998)