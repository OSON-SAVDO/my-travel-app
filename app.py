from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ТОКЕНИ ХУДРО ИНҶО ГУЗОР
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
        # Истифодаи API-и нархҳои арзон
        url = "https://api.travelpayouts.com/v1/prices/cheap"
        params = {
            'origin': origin.upper(),
            'destination': destination.upper(),
            'currency': currency,
            'token': API_TOKEN
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('success'):
                results = data.get('data', {})
                # API-и 'cheap' маълумотро дар дохили коди шаҳр медиҳад
                dest_data = results.get(destination.upper(), {})
                if dest_data:
                    # Табдил додани дикшенери ба рӯйхат барои HTML
                    for key, flight in dest_data.items():
                        flights.append(flight)
                else:
                    error_msg = "Дар ин самт ҳоло чиптаҳои арзон ёфт нашуданд."
            else:
                error_msg = f"Хатогии API: {data.get('error', 'Номаълум')}"
                
        except Exception as e:
            error_msg = f"Хатогии пайвастшавӣ: {str(e)}"

    return render_template('index.html', flights=flights, lang=lang, currency=currency, error_msg=error_msg)
