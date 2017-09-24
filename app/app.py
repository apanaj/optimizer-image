from flask import Flask, request, jsonify, send_file
import subprocess
import uuid
import re
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
        return jsonify({'error': 'The `url` parameter is required'}), 400

    disassembled = urlparse(url)
    orig_filename, file_ext = splitext(basename(disassembled.path))

    if not file_ext:
        return jsonify({'error': 'The `url` parameter is not valid'}), 400

    quality = request.args.get('q', 75)

    out_type = request.args.get('out_type')
    if out_type not in [None, 'crop', 'resize', 'force_resize']:
        return jsonify({'error': "The `out_type` is not valid. "
                                 "['crop', 'resize', 'force_resize'] "}), 400

    size = request.args.get('size')
    if out_type and size is None:
        return jsonify({'error': 'The `size` parameter is required'}), 400

    if size and not re.search(r'^(\d*\.*\d+|)x(\d*\.*\d+|)$', size):
        return jsonify({'error': 'The `size` parameter is not valid. (`width`x`height`) '}), 400

    options = ''
    if out_type == 'crop':
        options = '-gravity center -crop {}+0+0'.format(size)
    elif out_type == 'resize':
        options = '-resize {}'.format(size)
    elif out_type == 'force_resize':
        options = '-resize {}!'.format(size)

    # ---------- wget command ----------
    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = SOURCE_FOLDER + saved_filename
    cmd_download_image = 'wget --no-check-certificate -O {filepath} {url}'.format(
        filepath=source_filepath, url=url)
    subprocess.Popen(cmd_download_image, shell=True).communicate()

    # ---------- optimize command ----------
    optimized_filepath = OPTIMIZED_FOLDER + saved_filename
    optimize_cmd = "/home/majid/mozjpeg/cjpeg -quality {quality} {source_path} > {destination_path}".format(
        quality=quality,
        source_path=source_filepath,
        destination_path=optimized_filepath
    )
    process = subprocess.Popen(optimize_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # ---------- convert command ----------
    convert_cmd = "convert {input_file} {output_option} {output_file}".format(
        input_file=optimized_filepath,
        output_option=options,
        output_file=optimized_filepath
    )
    process = subprocess.Popen(convert_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return send_file(optimized_filepath, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
