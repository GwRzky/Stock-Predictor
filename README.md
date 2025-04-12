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
   ```bash
   git clone https://github.com/GustyCube/Stock-Predictor.git
   cd market-analysis-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following API keys:
   ```plaintext
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
   ```bash
   python run.py
   ```

6. Open your browser and navigate to:
   ```plaintext
   http://localhost:5000
   ```

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [News API](https://newsapi.org/)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap](https://getbootstrap.com/)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements.

Feel free to suggest edits or report issues for any further improvements.
