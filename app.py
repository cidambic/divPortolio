from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import yfinance as yf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)

# Define a list of stocks to analyze
stocks = ['AAPL', 'MSFT', 'JNJ', 'VZ', 'T', 'KO', 'PEP', 'PG', 'MMM', 'XOM']

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_basis = db.Column(db.Float, nullable=False)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        cost_basis = float(request.form['cost_basis'])
        stock = Stock(symbol=symbol, quantity=quantity, cost_basis=cost_basis)
        db.session.add(stock)
        db.session.commit()
        return redirect(url_for('index'))

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

    # Retrieve the list of stocks in the portfolio and calculate the total value
    portfolio = Stock.query.all()
    portfolio_value = 0
    for stock in portfolio:
        ticker = yf.Ticker(stock.symbol)
        data = ticker.history(period="max")
        latest_close_price = data['Close'][-1]
        stock_value = stock.quantity * latest_close_price
        portfolio_value += stock_value

    # Render the HTML template with the dividend table and portfolio
    return render_template('index.html', dividend_table=dividend_table, portfolio=portfolio, portfolio_value=portfolio_value)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

