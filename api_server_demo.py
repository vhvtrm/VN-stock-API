"""
Flask API Server for Vietnamese Stock Prices - DEMO VERSION
Uses mock data so you can test without database connection
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for browser access

# Mock stock data
MOCK_STOCKS = {
    'VNM': {'name': 'Vinamilk', 'base_price': 67800},
    'VIC': {'name': 'Vingroup', 'base_price': 42500},
    'VHM': {'name': 'Vinhomes', 'base_price': 65000},
    'TCB': {'name': 'Techcombank', 'base_price': 28000},
    'VPB': {'name': 'VPBank', 'base_price': 23500},
    'HPG': {'name': 'Hoa Phat Group', 'base_price': 24800},
    'MWG': {'name': 'Mobile World', 'base_price': 52000},
    'FPT': {'name': 'FPT Corporation', 'base_price': 128000},
    'MSN': {'name': 'Masan Group', 'base_price': 67500},
    'SSI': {'name': 'SSI Securities', 'base_price': 45000}
}


def generate_mock_price(symbol):
    """Generate realistic mock stock data"""
    if symbol not in MOCK_STOCKS:
        return None

    base_price = MOCK_STOCKS[symbol]['base_price']

    # Add some random variation
    price_change_pct = random.uniform(-3, 3)  # -3% to +3%
    current_price = base_price * (1 + price_change_pct / 100)

    # Generate OHLC
    open_price = base_price * (1 + random.uniform(-1, 1) / 100)
    high_price = max(open_price, current_price) * (1 + random.uniform(0, 2) / 100)
    low_price = min(open_price, current_price) * (1 - random.uniform(0, 2) / 100)

    change = current_price - base_price
    pct_change = (change / base_price) * 100

    return {
        'ticker': symbol,
        'symbol': symbol,
        'price': round(current_price, 2),
        'close_price': round(current_price, 2),
        'open': round(open_price, 2),
        'open_price': round(open_price, 2),
        'high': round(high_price, 2),
        'high_price': round(high_price, 2),
        'low': round(low_price, 2),
        'low_price': round(low_price, 2),
        'volume': random.randint(500000, 5000000),
        'change': round(change, 2),
        'change_amount': round(change, 2),
        'pct_change': round(pct_change, 2),
        'change_percent': round(pct_change, 2),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'trade_date': datetime.now().strftime('%Y-%m-%d')
    }


def generate_history(symbol, days):
    """Generate mock historical data"""
    history = []
    base_price = MOCK_STOCKS.get(symbol, {'base_price': 50000})['base_price']

    for i in range(days):
        date = datetime.now() - timedelta(days=days - i - 1)
        day_variation = random.uniform(-2, 2) / 100
        price = base_price * (1 + day_variation)

        history.append({
            'ticker': symbol,
            'trade_date': date.strftime('%Y-%m-%d'),
            'open_price': round(price * (1 + random.uniform(-1, 1) / 100), 2),
            'high_price': round(price * (1 + random.uniform(0, 2) / 100), 2),
            'low_price': round(price * (1 - random.uniform(0, 2) / 100), 2),
            'close_price': round(price, 2),
            'volume': random.randint(500000, 5000000),
            'change_amount': round(random.uniform(-500, 500), 2),
            'change_percent': round(random.uniform(-2, 2), 2)
        })

    return history


# --------------------------------------------------------------------------------
# API ENDPOINTS
# --------------------------------------------------------------------------------

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Vietnamese Stock Price API is running (DEMO MODE)'
    })


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """Get latest price for a single stock"""
    try:
        symbol = symbol.upper()
        price = generate_mock_price(symbol)

        if price:
            return jsonify({
                'success': True,
                'data': price
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No data found for symbol {symbol}'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stocks', methods=['POST'])
def get_multiple_stocks():
    """Get prices for multiple stocks"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if not symbols:
            return jsonify({
                'success': False,
                'error': 'symbols array is required'
            }), 400

        prices = {}
        for symbol in symbols:
            prices[symbol.upper()] = generate_mock_price(symbol.upper())

        return jsonify({
            'success': True,
            'data': prices
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stock/<symbol>/history', methods=['GET'])
def get_stock_history(symbol):
    """Get historical prices for a stock"""
    try:
        days = request.args.get('days', default=30, type=int)
        symbol = symbol.upper()

        if days < 1 or days > 365:
            return jsonify({
                'success': False,
                'error': 'days must be between 1 and 365'
            }), 400

        if symbol not in MOCK_STOCKS:
            return jsonify({
                'success': False,
                'error': f'No data found for symbol {symbol}'
            }), 404

        history = generate_history(symbol, days)

        return jsonify({
            'success': True,
            'data': history,
            'count': len(history)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/market/<market_name>', methods=['GET'])
def get_market_summary(market_name):
    """Get summary of all stocks in a market"""
    try:
        market = market_name.upper()

        # Generate mock data for all stocks
        data = []
        for symbol in MOCK_STOCKS.keys():
            price = generate_mock_price(symbol)
            if price:
                data.append(price)

        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# --------------------------------------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# --------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    print("="*60)
    print("Vietnamese Stock Price API Server - DEMO MODE")
    print("="*60)
    print("\n⚠️  Using MOCK DATA (no database connection required)")
    print("\nAvailable Endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/stock/<symbol>")
    print("  POST /api/stocks")
    print("  GET  /api/stock/<symbol>/history?days=30")
    print("  GET  /api/market/<market>")
    print("\nAvailable Stock Symbols:")
    print(" ", ", ".join(MOCK_STOCKS.keys()))
    print("\n" + "="*60)
    print("\nStarting server on http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("\n✅ Open example_ai_app.html in your browser to test!")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5001, debug=False)
