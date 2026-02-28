import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ТОКЕНИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

@app.route('/')
def index():
    # Маълумоти аввалия барои интерфейс
    data_ui = {
        'origin': request.args.get('origin', 'DYU'),
        'dest': request.args.get('destination', 'MOW'),
        'curr': request.args.get('currency', 'TJS'),
        'lang': request.args.get('lang', 'tg')
    }
    
    flights = []
    # Ҷустуҷӯи чиптаҳо бо API-и V3 (Стандарти нав)
    if request.args.get('origin'):
        url = "https://api.travelpayouts.com/v3/prices_for_dates"
        params = {
            'origin': data_ui['origin'],
            'destination': data_ui['dest'],
            'currency': data_ui['curr'],
            'token': API_TOKEN,
            'limit': 10
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                flights = response.json().get('data', [])
        except Exception:
            pass

    return render_template('index.html', flights=flights, ui=data_ui)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
