from flask import Flask
from config import Config
from app.utils import nl2br

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.jinja_env.filters['nl2br'] = nl2br
    
    from app.services import init_services
    init_services(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app