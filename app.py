from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

# Луғати тарҷумаҳо
texts = {
    'tg': {'title': 'Ҷустуҷӯи чиптаҳо', 'from': 'Аз куҷо?', 'to': 'Ба куҷо?', 'search': 'Ҷустуҷӯ', 'price': 'Нарх', 'airline': 'Ширкат', 'date': 'Парвоз', 'buy': 'Харидан'},
    'ru': {'title': 'Поиск билетов', 'from': 'Откуда?', 'to': 'Куда?', 'search': 'Найти', 'price': 'Цена', 'airline': 'Авиакомпания', 'date': 'Вылет', 'buy': 'Купить'},
    'en': {'title': 'Flight Search', 'from': 'From?', 'to': 'To?', 'search': 'Search', 'price': 'Price', 'airline': 'Airline', 'date': 'Departure', 'buy': 'Buy'}
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'tg')
    currency = request.args.get('currency', 'TJS')
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    
    flights = []
    error_msg = None

    if origin and destination:
        url = "https://api.travelpayouts.com/v1/prices/cheap"
        params = {'origin': origin, 'destination': destination, 'currency': currency, 'token': API_TOKEN}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('success'):
                res = data.get('data', {}).get(destination, {})
                flights = [res[k] for k in res]
            else:
                error_msg = "Error API"
        except:
            error_msg = "Connection Error"

    return render_template('index.html', flights=flights, lang=lang, currency=currency, t=texts[lang], error_msg=error_msg)
