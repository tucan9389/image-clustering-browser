# Image Clustering Browser

You can cluster bunch of images with [faiss](https://github.com/facebookresearch/faiss) similarity and [k-means](https://en.wikipedia.org/wiki/K-means_clustering) clustering algorithm and browse the result on web with react client and flask server.

## DEMO

![clustering-viewer-demo-coco-dataset-3-3](https://user-images.githubusercontent.com/37643248/103138522-d0a10c00-4716-11eb-84d8-5bbe21e137f1.gif)

## Features

- Cluster (python 3.6+, faiss, k-means)

  - [x] Without copying images, cluster million level images and write at txt files
  - [ ] Make featuremaps with images

- Server (python 3.6+, flask)

  - [x] Serve hierarchical directories browsing api
  - [x] Serve images serving api

- Client (javscript, react)
  - [x] View the result of clustering with huge number of images
  - [x] Browse the hierarchical directories
  - [x] Show bunch of images with grid gallery view and paginization
- Others
  - [ ] Support to run and show the progress of the clustering with buttons on the web
  - [ ] Show the featuremaps for each image
  
## Diagram

<img src="https://user-images.githubusercontent.com/37643248/103156055-4c1ebe00-47e8-11eb-875e-4dcd0e70ad1c.png" width=500px>

## Getting Started

### 0. Clone the project

```shell script
$ git clone https://github.com/tucan9389/image-clustering-browser
```

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
3. Install python libraries for clustering batch and api server

```shell script
$ pip install numpy Flask Flask-Cors
```

4. [Install yarn](https://classic.yarnpkg.com/en/docs/install/) for react app

### 3. Get featuremaps

> Preparing...

```shell script
$
```

### 4. Run Clustering

```shell script
$ cd ~/image-clustering-browser/clustering
$ python clustering-to-txt.py \
    --number_of_cluster 100 \
    --img_dir_path "../data/my-images-001" \
    --featuremap_dir_path "../data/my-images-001-rexnetv1_2.0x-inferredfeatures" \
    --clustering_output_path "../data/clutering-results/my-images-001-clustering"
```

### 5. Run Browser API and Client Server

```shell script
# run api server
$ cd ~/image-clustering-browser/browser-server
$ python app.py \
    --img_dir_path "../data/my-images-001" \
    --clustering_output_path "../data/clutering-results/my-images-001-clustering"

# and then run client server
$ cd ~/image-clustering-browser/browser-react
$ yarn start
```

And now you can browse the clustered images at [`http://localhost:3000/browser/`](`http://localhost:3000/browser/`).

## Used Functions

- faiss
- k-means clustering
- ReXNetV1
- React
- Flask

## Reference
