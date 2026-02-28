import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ТОКЕНИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

CITIES = [
    {'name': 'Душанбе', 'code': 'DYU'}, 
    {'name': 'Хуҷанд', 'code': 'LBD'},
    {'name': 'Москва', 'code': 'MOW'}, 
    {'name': 'Истанбул', 'code': 'IST'}
]

@app.route('/')
def index():
    origin = request.args.get('origin', 'DYU')
    destination = request.args.get('destination', 'MOW')
    currency = request.args.get('currency', 'TJS')
    
    flights = []
    error_msg = None
    
    # Танҳо агар тугмаи ҷустуҷӯ пахш шавад, ба API дархост мефиристем
    if request.args.get('origin'):
        url = "https://api.travelpayouts.com/v1/prices/cheap"
        params = {'origin': origin, 'destination': destination, 'currency': currency, 'token': API_TOKEN}
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get('success'):
                res = data.get('data', {}).get(destination, {})
                flights = [res[k] for k in res]
            else:
                error_msg = "Маълумот ёфт нашуд"
        except:
            error_msg = "Хатогии пайвастшавӣ ба сервер"

    return render_template('index.html', flights=flights, currency=currency, cities=CITIES, error_msg=error_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
