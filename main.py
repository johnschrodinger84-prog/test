from flask import Flask, jsonify, render_template, request
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import blueprints
    from apps.OneClickTrip import bp as oneclicktrip_bp
    from apps.Calories import bp as calories_bp
    from apps.SchoolKiller import bp as schoolkiller_bp
    from apps.StyleTranslator import bp as styletranslator_bp
    from apps.core.main import bp as core_bp
    from apps.DietTracker.main import bp as diet_tracker_bp

    # Register blueprints
    app.register_blueprint(oneclicktrip_bp, url_prefix='/oneclicktrip')
    app.register_blueprint(calories_bp, url_prefix='/calories')
    app.register_blueprint(schoolkiller_bp, url_prefix='/schoolkiller')
    app.register_blueprint(styletranslator_bp, url_prefix='/styletranslator')
    app.register_blueprint(core_bp, url_prefix='/core')
    app.register_blueprint(diet_tracker_bp, url_prefix='/diet_tracker')

    # Root route - landing page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Handle all other routes
    @app.route('/<path:path>')
    def catch_all(path):
        # Check if the request is an API request
        if request.headers.get('Accept') == 'application/json' or \
           request.headers.get('Content-Type') == 'application/json' or \
           path.startswith(('oneclicktrip/', 'calories/', 'schoolkiller/', 'styletranslator/', 'core/')):
            return jsonify({'error': 'Not found'}), 404
        # For browser requests, redirect to home page
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        # Check if the request is an API request
        if request.headers.get('Accept') == 'application/json' or \
           request.headers.get('Content-Type') == 'application/json':
            return jsonify({'error': 'Not found'}), 404
        # For browser requests, redirect to home page
        return render_template('index.html')

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 