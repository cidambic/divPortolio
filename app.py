from flask import Flask, render_template
import pandas as pd
import numpy as np
import yfinance as yf

app = Flask(__name__)

# Define a list of stocks to analyze
stocks = ['AAPL', 'MSFT', 'JNJ', 'VZ', 'T', 'KO', 'PEP', 'PG', 'MMM', 'XOM']

@app.route("/")
def index():
    # Create an empty dataframe to store the stock data
    dividend_data = pd.DataFrame(columns=['Stock', 'Dividend Yield', 'Payout Ratio'])

    # Loop through the list of stocks, download the stock data from Yahoo Finance,
    # and calculate the dividend yield and payout ratio
    for stock in stocks:
        ticker = yf.Ticker(stock)
        data = ticker.history(period="max")
        latest_close_price = data['Close'][-1]
        dividend = ticker.dividends
        dividend_yield = np.mean(dividend) / latest_close_price
        net_income = ticker.earnings
        payout_ratio = np.mean(dividend) / np.mean(net_income)
        dividend_data = dividend_data.append({'Stock': stock, 'Dividend Yield': dividend_yield, 'Payout Ratio': payout_ratio}, ignore_index=True)

    # Sort the dataframe by dividend yield and convert to HTML table
    dividend_data = dividend_data.sort_values(by=['Dividend Yield'], ascending=False)
    dividend_table = dividend_data.to_html(index=False)

    # Render the HTML template with the dividend table
    return render_template('index.html', dividend_table=dividend_table)

if __name__ == '__main__':
    app.run(debug=True)
