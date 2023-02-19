# divPortolio
Build a dividend portfolio

This Flask app calculates the dividend yield and payout ratio for each stock in the list and sorts the results by dividend yield. The results are converted to an HTML table and displayed on the web page using a Jinja template. You can modify the list of stocks and adjust the criteria for selecting stocks based on your investment goals and risk tolerance. 

1. Install Flask and necessary libraries by running the command pip install -r requirements.txt.

2. Set up a Google Cloud Platform project and create OAuth 2.0 credentials. Save the credentials file as credentials.json in the root directory of the repository.

3. Set up a SQLite database by running the command python to start a Python shell, then running the following commands:

from app import db
db.create_all()

4. Run the flask app

python app.py

5. Open a web browser and navigate to http://localhost:5000 to see the table of the top dividend-paying stocks based on the list of stocks provided.

Requirements.txt
click==7.1.2
Flask==1.1.2
Flask-Login==0.5.0
Flask-SQLAlchemy==2.4.4
google-auth==1.30.0
google-auth-oauthlib==0.4.4
google-auth-httplib2==0.4.0
pandas==1.2.3
numpy==1.20.2
yfinance==0.1.59

