"""
Fetch Vietnamese stock prices using pymssql (no ODBC required)
"""

import pymssql
from database_connection_pymssql import get_connection
from datetime import datetime, timedelta


class StockPriceFetcher:
    """Fetch stock prices from DClab database using pymssql"""

    def __init__(self):
        """Initialize with database connection"""
        self.conn = get_connection()

    def get_latest_price(self, symbol):
        """Get the most recent price for a stock"""
        cursor = self.conn.cursor(as_dict=True)

        query = """
        SELECT TOP 1
            TICKER,
            PX_LAST as close_price,
            PX_OPEN as open_price,
            PX_HIGH as high_price,
            PX_LOW as low_price,
            VOLUME,
            TRADE_DATE
        FROM Market_Data
        WHERE TICKER = %s
        ORDER BY TRADE_DATE DESC
        """

        cursor.execute(query, (symbol,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            # Calculate change (compared to open)
            change = row['close_price'] - row['open_price']
            pct_change = (change / row['open_price'] * 100) if row['open_price'] else 0

            return {
                'symbol': row['TICKER'],
                'ticker': row['TICKER'],
                'price': float(row['close_price']),
                'open': float(row['open_price']),
                'high': float(row['high_price']),
                'low': float(row['low_price']),
                'volume': int(row['VOLUME']),
                'date': row['TRADE_DATE'].strftime('%Y-%m-%d'),
                'trade_date': row['TRADE_DATE'].strftime('%Y-%m-%d'),
                'close_price': float(row['close_price']),
                'open_price': float(row['open_price']),
                'high_price': float(row['high_price']),
                'low_price': float(row['low_price']),
                'change': float(change),
                'change_amount': float(change),
                'pct_change': round(pct_change, 2),
                'change_percent': round(pct_change, 2)
            }

        return None

    def get_multiple_prices(self, symbols):
        """Get prices for multiple stocks"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_latest_price(symbol)
        return results

    def get_price_history(self, symbol, days=30):
        """Get historical prices for a stock"""
        cursor = self.conn.cursor(as_dict=True)

        query = """
        SELECT TOP (%s)
            TICKER,
            PX_LAST as close_price,
            PX_OPEN as open_price,
            PX_HIGH as high_price,
            PX_LOW as low_price,
            VOLUME,
            TRADE_DATE
        FROM Market_Data
        WHERE TICKER = %s
        ORDER BY TRADE_DATE DESC
        """

        cursor.execute(query, (days, symbol))
        rows = cursor.fetchall()
        cursor.close()

        results = []
        for row in rows:
            change = row['close_price'] - row['open_price']
            pct_change = (change / row['open_price'] * 100) if row['open_price'] else 0

            results.append({
                'symbol': row['TICKER'],
                'ticker': row['TICKER'],
                'price': float(row['close_price']),
                'open': float(row['open_price']),
                'high': float(row['high_price']),
                'low': float(row['low_price']),
                'volume': int(row['VOLUME']),
                'date': row['TRADE_DATE'].strftime('%Y-%m-%d'),
                'trade_date': row['TRADE_DATE'].strftime('%Y-%m-%d'),
                'change': float(change),
                'pct_change': round(pct_change, 2)
            })

        return results

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    # Test
    with StockPriceFetcher() as fetcher:
        print("Testing VNM price:")
        vnm = fetcher.get_latest_price('VNM')
        if vnm:
            print(f"✅ {vnm['symbol']}: {vnm['price']:,.0f} VND ({vnm['pct_change']:+.2f}%)")
        else:
            print("❌ No data found")
