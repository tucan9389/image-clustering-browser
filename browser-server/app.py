from flask import Flask
from flask import send_file
from flask import jsonify
from flask import request
from flask_cors import CORS

import os
import argparse
import pathlib

IMG_NAMES_TXT_FILENAME = "img_names.txt"

app = Flask(__name__)
CORS(app)

@app.route('/image/<path:subpath>')
def get_image(subpath):
    img_path = os.path.join(args.img_dir_path, subpath)
    return send_file(img_path)  # , mimetype='image/gif')

@app.route('/browse/')
def get_files_and_directories_of_root():
    return get_files_and_directories(".")

def get_root_dir_name():
    clustering_output_path = str(args.clustering_output_path)
    dir_name = clustering_output_path.split("/")[-1]
    if clustering_output_path == "." or clustering_output_path == "./":
        return os.getcwd().split("/")[-1]
    elif len(dir_name) == 0 or dir_name == ".":
        return clustering_output_path.split("/")[-2]
    else:
        return dir_name

@app.route('/browse/<path:subpath>')
def get_files_and_directories(subpath):
    root_dir_name = get_root_dir_name()
    img_page = int(request.args.get('page', 1))
    num_per_page = int(request.args.get('num_per_page', 48))
    target_path = os.path.join(args.clustering_output_path, subpath)
    img_names_txt_file_path = os.path.join(target_path, IMG_NAMES_TXT_FILENAME)
    if os.path.exists(img_names_txt_file_path):
        with open(img_names_txt_file_path, "r") as text_file:
            image_names = text_file.read().split("\n")
            image_names = list(filter(lambda image_name: len(image_name) > 0, image_names))
    else:
        image_names = []

    img_page_idx = img_page - 1
    img_page_idx = img_page_idx if img_page_idx >= 0 else 0

    total_num_images = len(image_names)
    start_index = img_page_idx * num_per_page
    end_index = min((img_page_idx+1) * num_per_page, len(image_names))
    image_names = image_names[start_index: end_index]
    image_names = list(map(lambda image_name: os.path.join('/image', image_name), image_names))

    clustering_names = os.listdir(target_path)
    clustering_names = list(filter(lambda clustering_name: not clustering_name.startswith("."), clustering_names))
    clustering_names = list(filter(lambda clustering_name: clustering_name != IMG_NAMES_TXT_FILENAME, clustering_names))
    clustering_names.sort()

    total_pages = 0
    if total_num_images > 0:
        total_pages = int((total_num_images - 1) / num_per_page) + 1

    return jsonify({
        'root_dir_name': root_dir_name,
        'clu_names': clustering_names,
        'img_names': image_names,
        'is_last_img_page': end_index == total_num_images,
        'total_pages': total_pages,
        'total_images': total_num_images,
    })

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir_path', type=pathlib.Path, default='../data/clutering-results/mpii_human_pose_v1')
    parser.add_argument('--clustering_output_path', type=pathlib.Path, default='../data/clutering-results/mpii_human_pose_v1-clustering')

    args = parser.parse_args()

    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8001)
