from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ТОКЕНИ ХУДРО ИНҶО ГУЗОР
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

CITIES = [
    {'name': 'Душанбе', 'code': 'DYU'}, {'name': 'Хуҷанд', 'code': 'LBD'},
    {'name': 'Москва', 'code': 'MOW'}, {'name': 'Истанбул', 'code': 'IST'},
    {'name': 'Дубай', 'code': 'DXB'}, {'name': 'Тошканд', 'code': 'TAS'},
    {'name': 'Алмати', 'code': 'ALA'}, {'name': 'Франкфурт', 'code': 'FRA'}
]

TEXTS = {
    'tg': {'search': 'Ҷустуҷӯ', 'buy': 'Харидан', 'direct': 'Парвози мустақим', 'airline': 'Ширкат', 'dep': 'Парвоз'},
    'ru': {'search': 'Найти', 'buy': 'Купить', 'direct': 'Прямой рейс', 'airline': 'Компания', 'dep': 'Вылет'},
    'en': {'search': 'Search', 'buy': 'Buy Now', 'direct': 'Direct', 'airline': 'Airline', 'dep': 'Departure'}
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'tg')
    currency = request.args.get('currency', 'TJS')
    origin = request.args.get('origin', 'DYU')
    destination = request.args.get('destination', 'MOW')
    
    flights = []
    # Гирифтани рӯйхати зиёди чиптаҳо (Prices for Dates)
    url = "https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'currency': currency,
        'token': API_TOKEN,
        'limit': 15  # Нишон додани 15 чиптаи беҳтарин
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'data' in data:
            flights = data['data']
    except:
        pass

    return render_template('index.html', flights=flights, lang=lang, currency=currency, cities=CITIES, t=TEXTS[lang])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
