from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from MeteoData import MeteoData, MeteoOutput

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>ggfd689(dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)

meteo = MeteoData('Москва')
format_output = MeteoOutput()


@app.route('/', methods=['POST', 'GET'])
def index():
    global meteo, format_output
    # words = []
    # if request.is_json:
    #     data = request.get_json()
    #     if data.get('type'):
    #         words = data['data']
    if request.form['location']:
        meteo = MeteoData(request.form['location'])

    meteo_data = meteo.get_meteo_data()

    return render_template('index.html',
                           meteo_data=meteo_data,
                           hints=None, #meteo.get_hints(words),
                           format_output=format_output,
                           loc=meteo.get_location_data())


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=4998)
