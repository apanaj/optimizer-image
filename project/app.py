from flask import Flask, jsonify

from exceptions import FileNotFoundException, LargeFileException, \
    FileSizeException, CjpegConvertException
from views import mod


def create_app(config, app_name):
    app = Flask(app_name)
    app.config.from_object(config)
    app.register_blueprint(mod)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify(error='File is too large'), 413

    @app.errorhandler(LargeFileException)
    def large_file_exception(error):
        return jsonify(error='File is too large'), 413

    @app.errorhandler(FileSizeException)
    def file_size_exception(error):
        return jsonify(error='File size is not valid'), 400

    @app.errorhandler(CjpegConvertException)
    def cjpeg_convert_exception(error):
        return jsonify(error='The file type is not supported'), 400

    @app.errorhandler(FileNotFoundException)
    def file_not_found_exception(error):
        return jsonify(error='File not found'), 404

    return app
