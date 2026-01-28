"""
Flask API Server for Vietnamese Stock Prices
Exposes database queries as REST API endpoints for Google AI Studio integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from get_stock_prices import StockPriceFetcher
from datetime import datetime
import traceback

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
        'message': 'Vietnamese Stock Price API is running'
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
            'data': prices
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

        if history.empty:
            return jsonify({
                'success': False,
                'error': f'No historical data found for {symbol}'
            }), 404

        # Convert DataFrame to list of dicts
        data = history.to_dict('records')

        # Convert dates to strings
        for item in data:
            if 'trade_date' in item and item['trade_date']:
                item['trade_date'] = item['trade_date'].strftime('%Y-%m-%d')

        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/market/<market_name>', methods=['GET'])
def get_market_summary(market_name):
    """
    Get summary of all stocks in a market

    Example: GET /api/market/HOSE
    """
    try:
        valid_markets = ['HOSE', 'HNX', 'UPCOM']
        market = market_name.upper()

        if market not in valid_markets:
            return jsonify({
                'success': False,
                'error': f'Invalid market. Must be one of: {valid_markets}'
            }), 400

        f = get_fetcher()
        summary = f.get_market_summary(market)

        if summary.empty:
            return jsonify({
                'success': False,
                'error': f'No data found for market {market}'
            }), 404

        # Convert DataFrame to list of dicts
        data = summary.to_dict('records')

        # Convert dates to strings
        for item in data:
            if 'trade_date' in item and item['trade_date']:
                item['trade_date'] = item['trade_date'].strftime('%Y-%m-%d')

        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/search', methods=['GET'])
def search_stocks():
    """
    Search for stocks by keyword

    Example: GET /api/search?q=bank
    """
    try:
        query = request.args.get('q', '')

        if not query or len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Search query must be at least 2 characters'
            }), 400

        # This would require a company names table in the database
        # For now, return a placeholder
        return jsonify({
            'success': True,
            'data': [],
            'message': 'Search functionality requires company names table'
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
    print("Vietnamese Stock Price API Server")
    print("="*60)
    print("\nAvailable Endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/stock/<symbol>")
    print("  POST /api/stocks")
    print("  GET  /api/stock/<symbol>/history?days=30")
    print("  GET  /api/market/<market>")
    print("  GET  /api/search?q=keyword")
    print("\n" + "="*60)
    print("\nStarting server on http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5001, debug=False)
