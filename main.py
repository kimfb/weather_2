from flask import Flask, render_template, request, jsonify
from MeteoData import MeteoData, MeteoOutput

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>ggfd689(dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)

meteo = MeteoData('Москва')
format_output = MeteoOutput()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        meteo.update_req(request.form['location'])

    meteo_data = meteo.get_meteo_data()
    return render_template('index.html',
                           meteo_data=meteo_data,
                           format_output=format_output,
                           loc=meteo.get_location_data())


@app.route('/search', methods=['GET', 'POST'])
def search():
    hints = meteo.get_hints(request.json['data'])
    return jsonify(hints)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=4998)
