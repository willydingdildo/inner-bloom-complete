import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp

from src.routes.real_api import real_api_bp
from src.routes.initiation_api import initiation_bp
from src.routes.marketplace_api import marketplace_bp
from src.routes.addiction_api import addiction_bp
from src.routes.identity_api import identity_bp
from src.routes.social_proof_api import social_proof_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(real_api_bp, url_prefix='/api/real')
app.register_blueprint(initiation_bp, url_prefix='/api/real')
app.register_blueprint(marketplace_bp, url_prefix='/api/real/marketplace')
app.register_blueprint(addiction_bp, url_prefix='/api/real/addiction')
app.register_blueprint(identity_bp, url_prefix='/api/real/identity')
app.register_blueprint(social_proof_bp, url_prefix='/api/real/social')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


from src.models.user import User

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


