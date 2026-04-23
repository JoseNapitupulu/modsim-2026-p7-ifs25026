from flask import Flask, send_from_directory
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.description_routes import description_bp
from app.routes.motivation_routes import motivation_bp

def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="")
    CORS(app)
    Base.metadata.create_all(bind=engine)
    app.register_blueprint(description_bp)
    app.register_blueprint(motivation_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/ui")
    def ui():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/health")
    def health():
        return "API telah berjalan!"

    return app