import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


def fetch_and_plot_stock_data():
    # User inputs
    ticker_symbol = input("Enter the ticker symbol (e.g., 'GOOGL'): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Fetch data
    ticker_data = yf.Ticker(ticker_symbol)
    ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)

    # Calculate moving averages
    ticker_df['MA20'] = ticker_df['Close'].rolling(window=20).mean()
    ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()

    # Calculate MACD
    ticker_df['EMA12'] = ticker_df['Close'].ewm(span=12, adjust=False).mean()
    ticker_df['EMA26'] = ticker_df['Close'].ewm(span=26, adjust=False).mean()
    ticker_df['MACD'] = ticker_df['EMA12'] - ticker_df['EMA26']
    ticker_df['Signal'] = ticker_df['MACD'].ewm(span=9, adjust=False).mean()

    # Calculate RSI
    delta = ticker_df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    ticker_df['RSI'] = 100 - (100 / (1 + rs))

    # Plotting
    plt.figure(figsize=(14, 10))

    # Plot Close Price and Moving Averages
    plt.subplot(411)
    plt.plot(ticker_df['Close'], label='Close Price', color='blue')
    plt.plot(ticker_df['MA20'], label='20-Day MA', color='red')
    plt.plot(ticker_df['MA50'], label='50-Day MA', color='green')
    plt.title(f'Stock Prices and Moving Averages for {ticker_symbol}')
    plt.legend()

    # Plot Volume
    plt.subplot(412)
    plt.bar(ticker_df.index, ticker_df['Volume'], color='gray')
    plt.title('Trading Volume')

    # Plot MACD
    plt.subplot(413)
    plt.plot(ticker_df.index, ticker_df['MACD'], label='MACD', color='blue')
    plt.plot(ticker_df.index, ticker_df['Signal'], label='Signal', color='red')
    plt.title('MACD')
    plt.legend()

    # Plot RSI
    plt.subplot(414)
    plt.plot(ticker_df.index, ticker_df['RSI'], label='RSI', color='purple')
    plt.title('RSI')
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Candlestick chart
    mpf.plot(ticker_df, type='candle', style='charles',
             title=f'{ticker_symbol} Candlestick',
             ylabel='Price ($)')


# Call the function
fetch_and_plot_stock_data()
