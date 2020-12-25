import os
import argparse
import pathlib
from datetime import datetime
import multiprocessing

import numpy as np
import faiss

manager = multiprocessing.Manager()
shared_count_list = manager.list([0, 0])

IMG_NAMES_TXT_FILENAME = "img_names.txt"


def load_featuremaps_multi(args):
    image_names, featuremap_dir_path, max_number_of_data, total_batches = args

    np_feature_array = []

    total_number_of_images = len(image_names)
    echo_num = 50
    for idx, img_name in enumerate(image_names):
        shared_count_list[0] += 1
        # if max_number_of_data is not None and shared_count_list[0] >= max_number_of_data:
        #     break

        tmp_name = img_name.split(".")
        del tmp_name[-1]
        # featuremap
        featuremap_filename = ".".join(tmp_name) + ".pth"
        featuremap_path = os.path.join(featuremap_dir_path, featuremap_filename)
        try:
            featuremap = np.load(featuremap_path)
            featuremap = featuremap.squeeze(0)
        except:
            featuremap = None
        np_feature_array.append(featuremap)

        if ((shared_count_list[0] + 1) % echo_num) == 0:
            print("  >> loading...", shared_count_list[0] + 1, "/", max_number_of_data)

    shared_count_list[1] += 1
    print("BATCH DONE:", shared_count_list[1], "/", total_batches)

    return np_feature_array

def run_kmeans(x, nmb_clusters):
    """
    Args:
        x: data
        nmb_clusters (int): number of clusters
    Returns:
        list: ids of data in each cluster
    """
    n_data, d = x.shape
    # logging.info("running k-means clustering with k=%d"%nmb_clusters)
    # logging.info("embedding dimensionality is %d"%d)

    # faiss implementation of k-means
    clus = faiss.Clustering(d, nmb_clusters)
    clus.niter = 20
    clus.max_points_per_centroid = 10000000
    index = faiss.IndexFlatL2(d)
    if faiss.get_num_gpus() > 0:
        index = faiss.index_cpu_to_all_gpus(index)
    # perform the training
    clus.train(x, index)
    _, idxs = index.search(x, 1)

    return [int(n[0]) for n in idxs]

def write_clustering_result(clustering_output_path, number_of_cluster, cluster_indexes, image_names):
    num_data_each_cluster = list(
        map(lambda cluster_idx: len(list(filter(lambda ci: ci == cluster_idx, cluster_indexes))),
            range(number_of_cluster)))
    filtered_cluster_indexes_pair = list(filter(lambda element: element[1] > 1, enumerate(num_data_each_cluster)))
    filtered_cluster_indexes_pair.sort(key=lambda pair: pair[1], reverse=True)
    print(filtered_cluster_indexes_pair)
    filtered_cluster_indexes = list(map(lambda element: element[0], filtered_cluster_indexes_pair))
    cluster_indexes = list(map(lambda cluster_index: "{:03d}".format(cluster_index), cluster_indexes))
    cluster_indexes = list(map(
        lambda cluster_index_str: cluster_index_str if int(cluster_index_str) in filtered_cluster_indexes else "etc",
        cluster_indexes))
    total_indexes = len(cluster_indexes)

    print("start to gather all image_name with cluster name")
    image_names_dict = {}
    for idx in range(total_indexes):
        cluster_name = cluster_indexes[idx]
        image_name = image_names[idx]

        if cluster_name in image_names_dict:
            image_names_dict[cluster_name].append(image_name)
        else:
            image_names_dict[cluster_name] = [image_name]
    print("end to gather all image_name with cluster name")

    print("start to sort the clusters")
    cluster_names = list(image_names_dict.keys())
    cluster_names.sort()
    print("end to sort the clusters")

    print("start to write image_names for each cluster")
    echo_num = 10
    total_num = len(cluster_names)
    for idx, cluster_name in enumerate(cluster_names):
        image_names = image_names_dict[cluster_name]

        cluster_dir_path = os.path.join(clustering_output_path, cluster_name)
        if not os.path.exists(cluster_dir_path):
            os.mkdir(cluster_dir_path)

        img_path = os.path.join(cluster_dir_path, IMG_NAMES_TXT_FILENAME)
        f = open(img_path, "w")
        f.write("\n".join(image_names))
        f.close()

        if (idx + 1) % echo_num == 0:
            print("  >> write done", idx + 1, "/", total_num)
    print("end to write image_names for each cluster")

def clustering_to_txt(number_of_cluster, img_dir_path, featuremap_dir_path, clustering_output_path, workers=48):
    assert number_of_cluster > 1, "--number_of_cluster > 1"
    assert os.path.exists(img_dir_path), "not exist: " + str(img_dir_path)
    assert os.path.exists(featuremap_dir_path), "not exist: " + str(featuremap_dir_path)

    print("START CLUSTERING")

    if not os.path.exists(clustering_output_path):
        os.mkdir(clustering_output_path)
        print(">> created directory:", clustering_output_path)

    # clustering 대상 txt 만들기
    img_names_txt_file_path = os.path.join(clustering_output_path, IMG_NAMES_TXT_FILENAME)
    if not os.path.exists(img_names_txt_file_path):
        print("start to write:", img_names_txt_file_path)
        image_names = os.listdir(img_dir_path)
        image_names = list(filter(lambda image_name: not image_name.startswith("."), image_names))
        with open(img_names_txt_file_path, "w") as text_file:
            text_file.write("\n".join(image_names))
        print("end to write:", img_names_txt_file_path)
    else:
        with open(img_names_txt_file_path, "r") as text_file:
            image_names = text_file.read().split("\n")
            image_names = list(filter(lambda image_name: len(image_name) > 0, image_names))

    max_number_of_data = len(image_names)  # 500  #

    # {날짜}-{시간}-{데이터갯수} 폴더에 저장
    current_log_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    current_log_name += "-d" + str(max_number_of_data)
    current_log_name += "-c" + str(number_of_cluster)

    clustering_output_path = os.path.join(clustering_output_path, current_log_name)
    os.mkdir(clustering_output_path)

    print("-" * 50)
    print("start to load featuremaps and images")

    image_names_list = [[]]  # list(map(lambda worker_idx: [], range(workers)))
    for idx, image_name in enumerate(image_names):
        if idx == max_number_of_data:
            break
        if len(image_names_list[-1]) >= int((max_number_of_data / (workers * 4))):
            image_names_list.append([])
        image_names_list[-1].append(image_name)
        # image_names_list[idx % workers].append(image_name)

    shared_count_list[0] = 0
    shared_count_list[1] = 0
    args_list = list(map(lambda image_names: (image_names, featuremap_dir_path, max_number_of_data, len(image_names_list)), image_names_list))
    pool = multiprocessing.Pool(processes=workers)
    np_feature_array_batch = pool.map(load_featuremaps_multi, args_list)

    # get remove indexes
    f_index = 0
    r_indexes = []
    for np_feature_array in reversed(np_feature_array_batch):
        for np_feature in reversed(np_feature_array):
            if np_feature is None:
                r_indexes.append(f_index)
            f_index += 1
    total_num = f_index
    r_indexes = list(map(lambda r_index: (total_num - r_index) - 1, r_indexes))
    print("total num before load:", len(image_names))
    for i in r_indexes:
        del image_names[i]
    print("total num after load:", len(image_names))
    np_feature_array_batch = list(map(lambda np_feature_array: list(filter(lambda np_feature: np_feature is not None, np_feature_array)), np_feature_array_batch))

    total_np_feature_array = []
    for np_feature_array in np_feature_array_batch:
        total_np_feature_array += np_feature_array
    print(len(total_np_feature_array))
    features = np.array(total_np_feature_array)
    print(features.shape)

    print("end to load featuremaps and images")
    print("-" * 50)

    print("-" * 50)
    print("start to cluster with k-means")
    cluster_indexes = run_kmeans(features, nmb_clusters=number_of_cluster)
    print("end to cluster with k-means")
    print("-" * 50)

    # write img_names.txt for each cluster
    write_clustering_result(clustering_output_path, number_of_cluster, cluster_indexes, image_names)

    print("-" * 50)
    print("-" * 50)
    print("-" * 50)
    print("ALL DONE and output is made at:", clustering_output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--number_of_cluster', type=int, default=100)
    parser.add_argument('--img_dir_path', type=pathlib.Path, default='../data/clutering-results/mpii_human_pose_v1')
    parser.add_argument('--featuremap_dir_path', type=pathlib.Path, default='../data/clutering-results/mpii_human_pose_v1-rexnetv1_2-inferredfeatures')
    parser.add_argument('--clustering_output_path', type=pathlib.Path, default='../data/clutering-results/mpii_human_pose_v1-clustering')

    args = parser.parse_args()

    clustering_to_txt(
        args.number_of_cluster,
        args.img_dir_path,
        args.featuremap_dir_path,
        args.clustering_output_path,
        workers=10
    )

