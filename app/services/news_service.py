from newsapi import NewsApiClient
from flask import current_app
from datetime import datetime, timedelta

def get_news(topic='stocks', days=7):
    """
    Fetch news articles about a specific topic using News API
    """
    api_key = current_app.config['NEWS_API_KEY']
    print(f"DEBUG - NEWS API KEY: {api_key}")  
    
    newsapi = NewsApiClient(api_key="INSERTAPIKEYHERE")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        data = newsapi.get_everything(
            q=topic,
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            language='en',
            sort_by='popularity',
            page_size=10  
        )
        
        if data.get('status') != 'ok':
            return {'error': data.get('message', 'Unknown error')}
        
        articles = data.get('articles', [])
        
        processed_articles = []
        for article in articles:
            processed_articles.append({
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'source': article.get('source', {}).get('name'),
                'published_at': article.get('publishedAt'),
                'content': article.get('content')
            })
        
        return {
            'articles': processed_articles,
            'total_results': data.get('totalResults'),
            'topic': topic
        }
    except Exception as e:
        return {'error': str(e)}