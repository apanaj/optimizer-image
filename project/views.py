import subprocess
import uuid
import re
from flask import Blueprint, request, current_app, jsonify, send_file
from urllib.parse import urlparse
from os.path import splitext, basename

from exceptions import FileNotFoundException, FileSizeException, \
    LargeFileException

mod = Blueprint('views', __name__)


def save_image_from_url(url):
    disassembled = urlparse(url)
    orig_filename, file_ext = splitext(basename(disassembled.path))

    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = current_app.config['SOURCE_FOLDER'] + saved_filename

    cmd_check_size = "wget --no-check-certificate --spider {url} 2>&1 | awk '/Length: / {{print $2;}}'; exit 0".format(
        url=url)
    filesize = subprocess.check_output(
        cmd_check_size,
        stderr=subprocess.STDOUT,
        shell=True)

    if not filesize:
        raise FileNotFoundException

    try:
        filesize = int(filesize)
    except ValueError:
        raise FileSizeException

    if filesize > current_app.config['MAX_CONTENT_LENGTH']:
        raise LargeFileException

    cmd_download_image = "wget --no-check-certificate -O {filepath} {url}".format(
        filepath=source_filepath, url=url)
    subprocess.Popen(cmd_download_image, shell=True).communicate()

    return source_filepath


def save_image_from_form(file):
    orig_filename, file_ext = splitext(basename(file.filename))
    saved_filename = str(uuid.uuid4()) + file_ext
    source_filepath = current_app.config['SOURCE_FOLDER'] + saved_filename
    file.save(source_filepath)
    return source_filepath


def image_optimizer(filename, tag, out_type, size, quality):
    source_filepath = filename
    convert_filepath = current_app.config['CONVERT_FOLDER'] + 'convert-' + basename(filename)
    optimized_filepath = current_app.config['OPTIMIZED_FOLDER'] + 'optimize-' + basename(filename)

    if tag:
        out_type = tag['out_type']
        quality = tag['quality']
        size = tag['size']

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
    optimize_cmd = current_app.config[
                       'MOZJPEG_FOLDER'] + "cjpeg -quality {quality} {source_filepath} > {destination_filepath}".format(
        quality=quality,
        source_filepath=source_filepath,
        destination_filepath=optimized_filepath
    )
    subprocess.run(optimize_cmd, shell=True)

    # ---------- Step 4- return optimized image file
    return send_file(optimized_filepath, mimetype='image/jpg')


@mod.route('/', methods=['GET', 'POST'])
def optimize():
    tag_param = request.args.get('tag')
    tag = current_app.config['OPTIMIZE_TAGS'].get(tag_param.lower()) \
        if tag_param else None
    if tag_param and tag is None:
        return jsonify({'error': '`tag` is not valid'}), 400

    out_type = request.args.get('type')
    size = request.args.get('size')
    quality = request.args.get('q')

    if request.method == 'POST':
        filename = save_image_from_form(request.files['file'])

        if 'type' in request.form:
            out_type = request.form['type']
        if 'size' in request.form:
            size = request.form['size']
        if 'q' in request.form:
            quality = request.form['q']
    else:
        url = request.args.get('url')
        disassembled = urlparse(url)
        orig_filename, file_ext = splitext(basename(disassembled.path))
        if not file_ext:
            return jsonify({'error': '`file extension` is not valid'}), 400

        filename = save_image_from_url(url)

    return image_optimizer(filename, tag, out_type, size, quality)
