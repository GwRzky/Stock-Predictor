import openai
from flask import current_app
import json
from datetime import datetime, timedelta
import requests
import re

from app.services.market_service import get_general_market_data

def analyze_general_market_with_type(news_data, analysis_type='general', budget=1000, topic='market finance economy'):
    """
    Use OpenAI to analyze market trends and news with a given analysis type, budget, and topic
    """
    try:
        openai_api_key = current_app.config['OPENAI_API_KEY']
        client = openai.OpenAI(api_key=openai_api_key)

        market_data = get_general_market_data(index_limit=5, crypto_limit=5)

        if 'error' in news_data:
            return {'error': f"News data error: {news_data['error']}"}

        articles = news_data.get('articles', [])
        article_titles = [article.get('title', '') for article in articles]
        article_descriptions = [article.get('description', '') for article in articles]

        timeframe = "current market conditions"
        if analysis_type == 'short_term':
            timeframe = "short-term market outlook (1-12 weeks), profit centric"
        elif analysis_type == 'long_term':
            timeframe = "long-term market outlook (1+ years), growth centric"

        prompt = f"""
You are a financial advisor. Based on the budget, market data, and news, provide an actionable analysis.

Investor topics of interest: {topic}
Investment budget: ${budget} USD
Desired analysis: {timeframe}

Recent Market Index Data:
{json.dumps([{
    'name': idx['name'], 
    'current_price': idx['current_price'],
    'change_percent': round(idx['change_percent'], 2),
    'trend': idx['trend']
} for idx in market_data['indices']], indent=2)}

Recent Cryptocurrency Data:
{json.dumps([{
    'name': crypto['name'], 
    'current_price': crypto['current_price'],
    'change_percent': round(crypto['change_percent'], 2),
    'trend': crypto['trend']
} for crypto in market_data['cryptos']], indent=2)}

News Headlines:
{json.dumps(article_titles[:10], indent=2)}

News Summaries:
{json.dumps(article_descriptions[:10], indent=2)}

Please provide your analysis in the following format with clear section breaks:

SUMMARY:
[Provide a concise executive summary of the overall market situation]

INDEX_RECOMMENDATIONS:
[Provide specific buy/sell/hold recommendations for the market indices with clear rationale]

CRYPTO_RECOMMENDATIONS:
[Provide specific buy/sell/hold recommendations for cryptocurrencies with clear rationale]

RISKS_OPPORTUNITIES:
[Outline the key risks and opportunities in the current market environment]

RECOMMENDED_INVESTMENT_STRATEGY:
[Provide a recommended investment strategy based on analysis. All assets — including individual stocks, indices, and cryptocurrencies — must be followed by their ticker or symbol in parentheses the first time and every time they are referenced (e.g., Microsoft (MSFT), Bitcoin (BTC), S&P 500 Index (SPX)). Do not skip any. This formatting rule is mandatory. Include expected timeframes and potential returns. Response should be multi-paragraph and detailed.]"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced financial analyst. Provide structured, clear, and practical market insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1800,
            temperature=0.4
        )

        analysis_text = response.choices[0].message.content

        # Section parser
        def extract_section(label, fallback="Not available."):
            pattern = fr"{label}:(.*?)(?=\n[A-Z_]+:|$)"
            match = re.search(pattern, analysis_text, re.DOTALL)
            return match.group(1).strip() if match else fallback

        analysis = {
            'analysis_text': analysis_text,
            'summary': extract_section("SUMMARY"),
            'index_recommendations': extract_section("INDEX_RECOMMENDATIONS"),
            'crypto_recommendations': extract_section("CRYPTO_RECOMMENDATIONS"),
            'risks_opportunities': extract_section("RISKS_OPPORTUNITIES"),
            'investment_strategy': extract_section("RECOMMENDED_INVESTMENT_STRATEGY"),
            'market_indices': market_data['indices'],
            'cryptocurrencies': market_data['cryptos'],
            'analyzed_news_count': len(articles[:10]),
            'analysis_type': analysis_type,
            'budget': budget,
            'topic': topic
        }

        return analysis

    except Exception as e:
        return {'error': str(e)}

def analyze_general_market(news_data):
    """
    Use OpenAI to analyze general market trends and news
    """
    return analyze_general_market_with_type(news_data, 'general')