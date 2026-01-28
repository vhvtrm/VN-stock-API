"""
Get Vietnamese Stock Prices from DClab Database - Simple Version
Direct connection without Entra ID authentication
"""

from database_connection_simple import connect_to_database
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd


class StockPriceFetcher:
    """Fetch stock prices from DClab database"""

    def __init__(self):
        """Initialize with database connection"""
        self.conn = None

    def connect(self):
        """Connect to database"""
        if not self.conn:
            self.conn = connect_to_database()
        return self.conn

    def get_latest_price(self, symbol: str) -> Optional[Dict]:
        """
        Get the latest price for a stock symbol

        Args:
            symbol: Stock ticker (e.g., 'VNM', 'VIC')

        Returns:
            Dictionary with price information or None
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Query for latest price from Market_Data table
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
        WHERE TICKER = ?
        ORDER BY TRADE_DATE DESC
        """

        try:
            cursor.execute(query, (symbol.upper(),))
            row = cursor.fetchone()

            if row:
                # Calculate change from open to close
                change = row.close_price - row.open_price if row.close_price and row.open_price else 0
                pct_change = (change / row.open_price * 100) if row.open_price and row.open_price > 0 else 0

                return {
                    'symbol': row.TICKER,
                    'ticker': row.TICKER,
                    'price': round(row.close_price, 2) if row.close_price else 0,
                    'close_price': round(row.close_price, 2) if row.close_price else 0,
                    'open': round(row.open_price, 2) if row.open_price else 0,
                    'open_price': round(row.open_price, 2) if row.open_price else 0,
                    'high': round(row.high_price, 2) if row.high_price else 0,
                    'high_price': round(row.high_price, 2) if row.high_price else 0,
                    'low': round(row.low_price, 2) if row.low_price else 0,
                    'low_price': round(row.low_price, 2) if row.low_price else 0,
                    'volume': int(row.VOLUME) if row.VOLUME else 0,
                    'date': row.TRADE_DATE.strftime('%Y-%m-%d') if row.TRADE_DATE else None,
                    'trade_date': row.TRADE_DATE.strftime('%Y-%m-%d') if row.TRADE_DATE else None,
                    'change': round(change, 2),
                    'change_amount': round(change, 2),
                    'pct_change': round(pct_change, 2),
                    'change_percent': round(pct_change, 2)
                }

            return None

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
        finally:
            cursor.close()

    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Optional[Dict]]:
        """
        Get latest prices for multiple stocks

        Args:
            symbols: List of stock tickers

        Returns:
            Dictionary mapping symbols to price data
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_latest_price(symbol)
        return results

    def get_price_history(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """
        Get historical prices for a stock

        Args:
            symbol: Stock ticker
            days: Number of days of history

        Returns:
            Pandas DataFrame with price history
        """
        conn = self.connect()

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        query = """
        SELECT
            ticker,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            change_amount,
            change_percent
        FROM stock_prices
        WHERE ticker = ?
            AND trade_date >= ?
            AND trade_date <= ?
        ORDER BY trade_date ASC
        """

        try:
            df = pd.read_sql(
                query,
                conn,
                params=(symbol.upper(), start_date, end_date)
            )
            return df

        except Exception as e:
            print(f"Error fetching history for {symbol}: {e}")
            return pd.DataFrame()

    def display_price(self, price_data: Dict):
        """Display price information"""
        if not price_data:
            print("No data available")
            return

        change_sign = '+' if price_data.get('change', 0) >= 0 else ''
        indicator = '🟢' if price_data.get('change', 0) >= 0 else '🔴'

        print(f"\n{'='*60}")
        print(f"{indicator} {price_data['symbol']}")
        print(f"{'='*60}")
        print(f"Price:        {price_data['price']:,.2f} VND")
        print(f"Change:       {change_sign}{price_data.get('change', 0):,.2f} ({change_sign}{price_data.get('pct_change', 0):.2f}%)")
        print(f"Open:         {price_data['open']:,.2f} VND")
        print(f"High:         {price_data['high']:,.2f} VND")
        print(f"Low:          {price_data['low']:,.2f} VND")
        print(f"Volume:       {price_data['volume']:,.0f}")
        print(f"Date:         {price_data['date']}")
        print(f"{'='*60}\n")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


def main():
    """Example usage"""
    print("Vietnamese Stock Price Fetcher - DClab Database (Simple Connection)")
    print("="*60)
    print()

    fetcher = StockPriceFetcher()

    try:
        # Example 1: Get single stock
        print("Example 1: Get latest price for VNM")
        print("-" * 60)
        vnm = fetcher.get_latest_price('VNM')
        if vnm:
            fetcher.display_price(vnm)

        # Example 2: Get multiple stocks
        print("\nExample 2: Get multiple stocks")
        print("-" * 60)
        symbols = ['VIC', 'VHM', 'TCB', 'VPB']
        prices = fetcher.get_multiple_prices(symbols)

        for symbol, data in prices.items():
            if data:
                fetcher.display_price(data)

    finally:
        fetcher.close()

    print("="*60)
    print("✅ Done!")
    print("="*60)


if __name__ == "__main__":
    main()
