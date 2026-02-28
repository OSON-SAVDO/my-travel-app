from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ТОКЕНИ ХУДРО АЗ TRAVELPAYOUTS ИНҶО ГУЗОР
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

CITIES = [
    {'name': 'Душанбе', 'code': 'DYU'},
    {'name': 'Хуҷанд', 'code': 'LBD'},
    {'name': 'Москва', 'code': 'MOW'},
    {'name': 'Истанбул', 'code': 'IST'},
    {'name': 'Дубай', 'code': 'DXB'},
    {'name': 'Тошканд', 'code': 'TAS'},
    {'name': 'Алмати', 'code': 'ALA'}
]

TEXTS = {
    'tg': {'title': 'Ҷустуҷӯи чиптаҳо', 'from': 'Аз куҷо?', 'to': 'Ба куҷо?', 'search': 'Ҷустуҷӯ', 'buy': 'Харидан', 'direct': 'Парвози мустақим'},
    'ru': {'title': 'Поиск билетов', 'from': 'Откуда?', 'to': 'Куда?', 'search': 'Найти', 'buy': 'Купить', 'direct': 'Прямой рейс'},
    'en': {'title': 'Flight Search', 'from': 'From?', 'to': 'To?', 'search': 'Search', 'buy': 'Buy', 'direct': 'Direct flight'}
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'tg')
    currency = request.args.get('currency', 'TJS')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    flights = []
    error_msg = None

    if origin and destination:
        url = "https://api.travelpayouts.com/v1/prices/cheap"
        params = {'origin': origin, 'destination': destination, 'currency': currency, 'token': API_TOKEN}
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get('success'):
                res = data.get('data', {}).get(destination, {})
                flights = [res[k] for k in res]
                if not flights:
                    error_msg = "Чипта ёфт нашуд."
            else:
                error_msg = "Хатогии API"
        except:
            error_msg = "Хатогии пайвастшавӣ"

    return render_template('index.html', flights=flights, lang=lang, currency=currency, cities=CITIES, t=TEXTS[lang], error_msg=error_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
