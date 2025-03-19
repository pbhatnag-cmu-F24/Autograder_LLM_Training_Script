from flask import Flask
from src.controllers.unzip_controller import unzip_bp
from src.controllers.file_filter_controller import filter_bp
from src.controllers.extraction_controller import dataset_extraction_bp
from src.controllers.dataset_processing_controller import dataset_processing_bp



app = Flask(__name__)
app.register_blueprint(unzip_bp, url_prefix="/api")
app.register_blueprint(filter_bp)
app.register_blueprint(dataset_extraction_bp)
app.register_blueprint(dataset_processing_bp)


if __name__ == "__main__":
    app.run(debug=True)
