from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ТОКЕНИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

CITIES = [
    {'name': 'Душанбе', 'code': 'DYU'}, {'name': 'Хуҷанд', 'code': 'LBD'},
    {'name': 'Москва', 'code': 'MOW'}, {'name': 'Истанбул', 'code': 'IST'},
    {'name': 'Дубай', 'code': 'DXB'}, {'name': 'Тошканд', 'code': 'TAS'},
    {'name': 'Алмати', 'code': 'ALA'}
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
    error_msg = None

    url = "https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'currency': currency,
        'token': API_TOKEN,
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            flights = data.get('data', [])
        else:
            error_msg = f"API Error: {response.status_code}"
    except Exception as e:
        error_msg = "Хатогии пайвастшавӣ"

    return render_template('index.html', flights=flights, lang=lang, currency=currency, cities=CITIES, t=TEXTS[lang], error_msg=error_msg)

# ИН ҚИСМ БАРОИ RENDER ХЕЛЕ МУҲИМ АСТ
if __name__ == '__main__':
    # Гирифтани порт аз системаи Render
    port = int(os.environ.get("PORT", 10000))
    # Истифодаи 0.0.0.0 барои дастрасии беруна
    app.run(host='0.0.0.0', port=port)
