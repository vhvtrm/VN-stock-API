"""
Get Vietnamese Stock Prices from DClab Database
Uses the database connection to fetch real stock market data
"""

from database_connection import connect_to_database
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

        # Query for latest price - adjust table/column names based on actual schema
        query = """
        SELECT TOP 1
            ticker,
            close_price,
            open_price,
            high_price,
            low_price,
            volume,
            trade_date,
            change_amount,
            change_percent
        FROM stock_prices
        WHERE ticker = ?
        ORDER BY trade_date DESC
        """

        try:
            cursor.execute(query, (symbol.upper(),))
            row = cursor.fetchone()

            if row:
                return {
                    'symbol': row.ticker,
                    'price': row.close_price,
                    'open': row.open_price,
                    'high': row.high_price,
                    'low': row.low_price,
                    'volume': row.volume,
                    'date': row.trade_date.strftime('%Y-%m-%d') if row.trade_date else None,
                    'change': row.change_amount,
                    'pct_change': row.change_percent
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

    def get_market_summary(self, market: str = 'HOSE') -> pd.DataFrame:
        """
        Get summary of all stocks in a market

        Args:
            market: Market name ('HOSE', 'HNX', 'UPCOM')

        Returns:
            DataFrame with all stocks' latest prices
        """
        conn = self.connect()

        query = """
        SELECT
            ticker,
            close_price,
            change_amount,
            change_percent,
            volume,
            trade_date
        FROM (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY trade_date DESC) as rn
            FROM stock_prices
            WHERE market = ?
        ) t
        WHERE rn = 1
        ORDER BY ticker
        """

        try:
            df = pd.read_sql(query, conn, params=(market,))
            return df

        except Exception as e:
            print(f"Error fetching market summary: {e}")
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
    print("Vietnamese Stock Price Fetcher - DClab Database")
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

        # Example 3: Get price history
        print("\nExample 3: Get 7-day price history for VNM")
        print("-" * 60)
        history = fetcher.get_price_history('VNM', days=7)
        if not history.empty:
            print(history.to_string(index=False))
        print()

    finally:
        fetcher.close()

    print("="*60)
    print("✅ Done!")
    print("="*60)


if __name__ == "__main__":
    main()
