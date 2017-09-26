import subprocess
import uuid
import re
from flask import Blueprint, request, current_app, jsonify, send_file
from urllib.parse import urlparse
from os.path import splitext, basename


mod = Blueprint('views', __name__)


def save_image_from_url(url):
    disassembled = urlparse(url)
    orig_filename, file_ext = splitext(basename(disassembled.path))

    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = current_app.config['SOURCE_FOLDER'] + saved_filename

    cmd_download_image = 'wget --no-check-certificate -O {filepath} {url}'.format(
        filepath=source_filepath, url=url)
    subprocess.Popen(cmd_download_image, shell=True).communicate()
    return source_filepath


def save_image_from_form(file):
    orig_filename, file_ext = splitext(basename(file.filename))
    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = current_app.config['SOURCE_FOLDER'] + saved_filename
    file.save(source_filepath)
    return source_filepath


def image_optimizer(filename, out_type, size, quality):
    source_filepath = filename
    convert_filepath = current_app.config['CONVERT_FOLDER'] + basename(filename)
    optimized_filepath = current_app.config['OPTIMIZED_FOLDER'] + basename(filename)
    quality = quality or 75

    # ---------- Step 1- argument validation
    if out_type not in [None, 'crop', 'resize', 'force_resize']:
        return jsonify({'error': "The `out_type` is not valid. "
                                 "['crop', 'resize', 'force_resize'] "}), 400

    if out_type and size is None:
        return jsonify({'error': 'The `size` parameter is required'}), 400

    if size and not re.search(r'^(\d*\.*\d+|)x(\d*\.*\d+|)$', size):
        return jsonify({'error': 'The `size` parameter is not valid. (`width`x`height`) '}), 400

    # ---------- Step 2- resize and crop with convert command
    if out_type:
        convert_options = ''
        if out_type == 'crop':
            convert_options = '-resize "{}^" -gravity center -crop "{}+0+0" -quality 100'.format(size, size)
        elif out_type == 'resize':
            convert_options = '-resize {}'.format(size)
        elif out_type == 'force_resize':
            convert_options = '-resize {}!'.format(size)

        convert_cmd = 'convert {input_file} {output_option} {output_file}'.format(
            input_file=source_filepath,
            output_option=convert_options,
            output_file=convert_filepath
        )
        subprocess.run(convert_cmd, shell=True)
        source_filepath = convert_filepath

    # ---------- Step 3- change image quality with optimize command
    optimize_cmd = "/home/majid/mozjpeg/cjpeg -quality {quality} {source_filepath} > {destination_filepath}".format(
        quality=quality,
        source_filepath=source_filepath,
        destination_filepath=optimized_filepath
    )
    subprocess.run(optimize_cmd, shell=True)

    # ---------- Step 4- return optimized image file
    return send_file(optimized_filepath, mimetype='image/jpg')


@mod.route('/opt', methods=['GET', 'POST'])
def optimize():
    if request.method == 'POST':
        try:
            filename = save_image_from_form(request.files['file'])
        except:
            return jsonify({'error': 'The `file` is not valid'}), 400
    else:
        try:
            url = request.args.get('url')
            disassembled = urlparse(url)
            orig_filename, file_ext = splitext(basename(disassembled.path))
            if not file_ext:
                return jsonify({'error': '`file extension` is not valid'}), 400

            filename = save_image_from_url(url)
        except:
            return jsonify({'error': 'The `url` parameter is not valid'}), 400

    out_type = request.args.get('type')
    size = request.args.get('size')
    quality = request.args.get('q')

    return image_optimizer(filename, out_type, size, quality)

