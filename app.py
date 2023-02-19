from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import yfinance as yf
from flask_dance.contrib.google import make_google_blueprint, google

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db = SQLAlchemy(app)

# Define a list of stocks to analyze
stocks = ['AAPL', 'MSFT', 'JNJ', 'VZ', 'T', 'KO', 'PEP', 'PG', 'MMM', 'XOM']

# Configure Google OAuth
blueprint = make_google_blueprint(client_id='client-id-goes-here', client_secret='client-secret-goes-here', offline=True, scope=['profile', 'email'])
app.register_blueprint(blueprint, url_prefix='/login')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_basis = db.Column(db.Float, nullable=False)

# Define the routes
@app.route("/")
def index():
    # If the user is not logged in, redirect to the login page
    if not google.authorized:
        return redirect(url_for('google.login'))
        
    # Get the user's information from Google
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    email = resp.json()['email']
    
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
    
    # Retrieve the list of stocks in the portfolio for the current user and calculate the total value
    portfolio = Stock.query.filter_by(email=email).all()
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

