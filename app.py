import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Танзимоти API
API_TOKEN = '71876b59812fee6e1539f9365e6a12dd'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
    origin = request.args.get('origin', 'DYU')
    destination = request.args.get('destination', 'MOW')
    
    url = f"https://api.travelpayouts.com/v3/prices_for_dates"
    params = {
        'origin': origin,
        'destination': destination,
        'token': API_TOKEN,
        'currency': 'TJS'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        return jsonify(response.json())
    except:
        return jsonify({"success": False, "error": "API Error"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
