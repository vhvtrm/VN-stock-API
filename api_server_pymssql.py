"""
Flask API Server for Vietnamese Stock Prices - Using pymssql (Railway compatible)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from get_stock_prices_pymssql import StockPriceFetcher
from datetime import datetime
import traceback
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Google AI Studio to access

# Initialize fetcher (reuse connection)
fetcher = None

def get_fetcher():
    """Get or create fetcher instance"""
    global fetcher
    if fetcher is None:
        fetcher = StockPriceFetcher()
    return fetcher


# --------------------------------------------------------------------------------
# API ENDPOINTS
# --------------------------------------------------------------------------------

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Vietnamese Stock Price API is running (REAL DATA)',
        'source': 'DClab Database',
        'driver': 'pymssql'
    })


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """
    Get latest price for a single stock

    Example: GET /api/stock/VNM
    """
    try:
        f = get_fetcher()
        price = f.get_latest_price(symbol.upper())

        if price:
            return jsonify({
                'success': True,
                'data': price,
                'source': 'real'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No data found for symbol {symbol}'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/stocks', methods=['POST'])
def get_multiple_stocks():
    """
    Get prices for multiple stocks

    Example: POST /api/stocks
    Body: {"symbols": ["VNM", "VIC", "VHM"]}
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if not symbols:
            return jsonify({
                'success': False,
                'error': 'symbols array is required'
            }), 400

        f = get_fetcher()
        prices = f.get_multiple_prices(symbols)

        return jsonify({
            'success': True,
            'data': prices,
            'source': 'real'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/stock/<symbol>/history', methods=['GET'])
def get_stock_history(symbol):
    """
    Get historical prices for a stock

    Example: GET /api/stock/VNM/history?days=30
    """
    try:
        days = request.args.get('days', default=30, type=int)

        if days < 1 or days > 365:
            return jsonify({
                'success': False,
                'error': 'days must be between 1 and 365'
            }), 400

        f = get_fetcher()
        history = f.get_price_history(symbol.upper(), days=days)

        if not history:
            return jsonify({
                'success': False,
                'error': f'No historical data found for {symbol}'
            }), 404

        return jsonify({
            'success': True,
            'data': history,
            'count': len(history),
            'source': 'real'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
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
    # Get port from environment variable (Railway) or default to 5001
    port = int(os.environ.get('PORT', 5001))

    print("="*60)
    print("Vietnamese Stock Price API Server - REAL DATA")
    print("="*60)
    print("\n⚠️  Using REAL DATABASE (DClab)")
    print("📦 Driver: pymssql (no ODBC required)")
    print("\nAvailable Endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/stock/<symbol>")
    print("  POST /api/stocks")
    print("  GET  /api/stock/<symbol>/history?days=30")
    print("\n" + "="*60)
    print(f"\nStarting server on http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=port, debug=False)
