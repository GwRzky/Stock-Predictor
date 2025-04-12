# Market Analysis with AI

This Flask application combines real-time market data with news and uses OpenAI's powerful AI to analyze trends and provide investment insights.

## Features

- Fetch real-time market data for any stock symbol
- Get the latest financial news on any topic
- AI-powered analysis that combines market data and news
- Interactive charts and visualizations
- User-friendly interface

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd market-analysis-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following API keys:
   ```
   OPENAI_API_KEY=
    ALPHA_VANTAGE_API_KEY=
    NEWS_API_KEY=
    FLASK_SECRET_KEY=
   ```

   You can obtain these API keys from:
   - [OpenAI](https://platform.openai.com/)
   - [Alpha Vantage](https://www.alphavantage.co/)
   - [News API](https://newsapi.org/)

5. Run the application:
   ```
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## License

MIT

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [News API](https://newsapi.org/)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap](https://getbootstrap.com/)