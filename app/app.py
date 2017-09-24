from flask import Flask, request, jsonify, send_file
import subprocess
import uuid
from urllib.parse import urlparse
from os.path import splitext, basename

app = Flask(__name__)

MEDIA_FOLDER = '/home/majid/temp/'
SOURCE_FOLDER = MEDIA_FOLDER + 'source/'
OPTIMIZED_FOLDER = MEDIA_FOLDER + 'optimized/'


@app.route('/opt')
def optimize():
    # URL validation and download file
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'The `url` parameter is required '}), 400

    disassembled = urlparse(url)
    orig_filename, file_ext = splitext(basename(disassembled.path))

    if not file_ext:
        return jsonify({'error': 'The `url` parameter is not valid '}), 400

    quality = request.args.get('q', 75)

    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = SOURCE_FOLDER + saved_filename
    cmd_download_image = 'wget --no-check-certificate -O {filepath} {url}'.format(
        filepath=source_filepath, url=url)

    print(cmd_download_image)
    args = cmd_download_image.split()
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Optimize Part
    optimized_filepath = OPTIMIZED_FOLDER + saved_filename
    optimize_cmd = "/home/majid/mozjpeg/cjpeg -quality {quality} {source_path} > {destination_path}".format(
        quality=quality,
        source_path=source_filepath,
        destination_path=optimized_filepath
    )
    process = subprocess.Popen(optimize_cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return send_file(optimized_filepath, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
