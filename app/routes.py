from flask import Blueprint, render_template, request, jsonify, current_app
from app.services.market_service import get_market_data
from app.services.news_service import get_news
from app.services.openai_service import analyze_general_market_with_type

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/market_data')
def market_data():
    symbol = request.args.get('symbol', 'AAPL')
    data = get_market_data(symbol)
    return render_template('market_data.html', data=data, symbol=symbol)

@main.route('/news')
def news():
    topic = request.args.get('topic', 'stocks')
    articles = get_news(topic)
    return render_template('news.html', articles=articles, topic=topic)

@main.route('/analysis')
def analysis():
    topic = request.args.get('topic', 'market finance economy stocks index crypto')
    analysis_type = request.args.get('analysis_type', 'general')
    budget = request.args.get('budget', '1000')
    generate = request.args.get('generate', 'false').lower() == 'true'

    print(f"[🔍 /analysis] generate={generate}, topic={topic}, analysis_type={analysis_type}")

    news_data = {}
    analysis_result = {}

    if generate:
        print("[⚙️ Generating analysis...]")
        try:
            news_data = get_news(topic)
            print(f"[📰 News fetched] Articles: {len(news_data.get('articles', []))}")
            analysis_result = analyze_general_market_with_type(news_data, analysis_type)
            print("[📊 Analysis complete]")
        except Exception as e:
            print(f"[❌ Error during analysis] {str(e)}")
    else:
        print("[ℹ️ Not generating — just rendering form page]")

    return render_template(
        'analysis.html',
        analysis=analysis_result,
        news_data=news_data,
        topic=topic,
        analysis_type=analysis_type,
        generate=generate,
        budget=budget
    )


@main.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    topic = data.get('topic', 'market finance economy stocks index crypto')
    analysis_type = data.get('analysis_type', 'general')
    
    news_data = get_news(topic)
    analysis = analyze_general_market_with_type(news_data, analysis_type)
    
    return jsonify({
        'analysis': analysis,
        'news_data': news_data
    })