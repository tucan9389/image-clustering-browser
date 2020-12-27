## Manual Clustering Guide

If you want to run clustering python script, you need to prepare the followings:
1. **target images** which are located on same path and same level, not heirarcical
2. **target featuremap** numpy files for eache image

This document shows how to prepare and make the directory structure.

### 1. Prepare Data

Download image data from what you want. You can prepare any bunch of unlabeled images like [ImageNet dataset](http://www.image-net.org/), [COCO dataset](https://cocodataset.org/#home), or your personal images in the mobile phone's photo album even though.

```
{path-to-your-working-directory}
├── image-clustering-browser # clone from this repo
|   ├── browser-react
|   ├── browser-server
|   ├── clustering
|   └── README.md
└── data                          # you shouldn't need to locate on the same level with the repo
    ├── my-images-001
    |   ├── img_001.jpg
    |   ├── img_002.jpg
    |   ├── ...
    |   └── img_999.jpg
    └── clutering-results
        └── my-images-001-clustering
            ├── 20201226-110202-d999-c50
            ├── 20201225-160650-d999-c100
            └── 20201225-170423-d999-c100
```

### 2. Install Requirements

1. [Install anaconda](https://docs.anaconda.com/anaconda/install/) and pathon 3.6+
2. [Install faiss](https://github.com/facebookresearch/faiss/blob/master/INSTALL.md) for clustering

### 3. Get featuremaps

> Preparing...

```shell script
$
```

### 4. Run Clustering

```shell script
$ cd clustering
$ python clustering-to-txt.py \
    --number_of_cluster 100 \
    --img_dir_path "../data/my-images-001" \
    --featuremap_dir_path "../data/my-images-001-rexnetv1_2.0x-inferredfeatures" \
    --clustering_output_path "../data/clutering-results/my-images-001-clustering"
```

## Final Directory Structure

```
../data/clutering-results
└── my-images-001-clustering
    ├── img_names.txt
    ├── 20201225-160650-d999-c5
    |   ├── 000
    |   |   └── img_names.txt
    |   ├── 001
    |   |   └── img_names.txt
    |   ├── 002
    |   |   └── img_names.txt
    |   ├── 004
    |   |   └── img_names.txt
    |   └── etc
    |       └── img_names.txt
    └── 20201225-170423-d999-c3
        ├── 000
        |   └── img_names.txt
        ├── 001
        |   └── img_names.txt
        |   └── 20201226-034123-d103-c3
        |       ├── 000
        |       |   └── img_names.txt
        |       ├── 001
        |       |   └── img_names.txt
        |       └── 002
        |           └── img_names.txt
        └── 002
            └── img_names.txt
```

## Used Libraries 

- [faiss](https://github.com/facebookresearch/faiss)
- [ReXNet](https://github.com/clovaai/rexnet)
