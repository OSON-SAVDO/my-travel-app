from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ТОКЕНИ ХУДРО АЗ TRAVELPAYOUTS ИНҶО ГУЗОР
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

@app.route('/')
def index():
    lang = request.args.get('lang', 'tg')
    currency = request.args.get('currency', 'TJS')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    flights = []
    error_msg = None

    if origin and destination:
        # Табдил додани кодҳои шаҳр ба ҳарфҳои калон (DYU, MOW)
        origin = origin.upper()
        destination = destination.upper()
        
        url = "https://api.travelpayouts.com/v3/prices_for_dates"
        params = {
            'origin': origin,
            'destination': destination,
            'currency': currency,
            'token': API_TOKEN,
            'format': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                flights = data.get('data', [])
                if not flights:
                    error_msg = "Дар ин самт чипта ёфт нашуд."
            elif response.status_code == 403:
                error_msg = "Хато: Токени API нодуруст аст ё фаъол нашудааст."
            else:
                error_msg = f"Хатогии API: {response.status_code}"
        except Exception as e:
            error_msg = f"Хатогии пайвастшавӣ: {str(e)}"

    return render_template('index.html', flights=flights, lang=lang, currency=currency, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)
