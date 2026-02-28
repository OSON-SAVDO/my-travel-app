from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# МАЪЛУМОТИ ХУДРО ИНҶО ГУЗОРЕД
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

@app.route('/')
def index():
    # Гирифтани танзимот аз корбар (забон ва асъор)
    lang = request.args.get('lang', 'tg')
    currency = request.args.get('currency', 'TJS')
    
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    flights = []
    if origin and destination:
        # Дархост ба API-и Travelpayouts
        url = f"https://api.travelpayouts.com/v3/prices_for_dates?origin={origin}&destination={destination}&currency={currency}&token={API_TOKEN}"
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            flights = data['data']

    return render_template('index.html', flights=flights, lang=lang, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)
