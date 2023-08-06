from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def frontend_index():
        return send_from_directory('../../webui', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../../webui', path)
    
    return app
