# Image Clustering Browser

You can browse clustered images on web. This repo also provides clustering with with [faiss](https://github.com/facebookresearch/faiss) similarity and [k-means](https://en.wikipedia.org/wiki/K-means_clustering) clustering algorithm.

## DEMO

![clustering-viewer-demo-coco-dataset-3-3](https://user-images.githubusercontent.com/37643248/103138522-d0a10c00-4716-11eb-84d8-5bbe21e137f1.gif)

## Features

- Server (python 3.6+, flask)

  - [x] Serve hierarchical directories browsing api
  - [x] Serve images serving api

- Client (javscript, react)
  - [x] View the result of clustering with huge number of images
  - [x] Browse the hierarchical directories
  - [x] Show bunch of images with grid gallery view and paginization
- Others
  - [x] Without copying images, cluster million level images and write at txt files (faiss)
  - [ ] Make featuremaps with images
  - [ ] Run clustering with buttons and show the progress of the task on the web
  - [ ] Show the featuremaps for each image
  
## Diagram

<img src="https://user-images.githubusercontent.com/37643248/103156156-407fc700-47e9-11eb-88be-4ac6b08e298c.png" width=600px>

## Getting Started

### 0. Clone the project

```shell script
$ git clone https://github.com/tucan9389/image-clustering-browser
cd image-clustering-browser
```

### 1. Install Requirements

1. [Install anaconda](https://docs.anaconda.com/anaconda/install/) and pathon 3.6+
3. Install python libraries for clustering batch and api server

```shell script
$ pip install numpy Flask Flask-Cors
```

4. [Install yarn](https://classic.yarnpkg.com/en/docs/install/) for react app
5. yarn install on browser-react directory

```shell script
$ cd browser-react
$ yarn install
```

### 2. Prepare Images and Clustering Result

You can select one of the options:

1. Download sample data from [image data](https://drive.google.com/drive/folders/1qY3i-JaR0txMU4UIuVJ65WKUCBQASEL6?usp=sharing) (19.31GB) and [clustering data](https://drive.google.com/drive/folders/1gHwcpuV8bp8-6PeNlyY5yazGIgY0SU7w?usp=sharing) (1.3MB)
2. Make your own clustering with [CLUSTERING_GUIDE.md](CLUSTERING_GUIDE.md)


<details>
<summary>The clustering makes the directory structure. If you make cluster by yourself, you have to conform the structure.</summary>

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
</details>

### 3. Run Browser API and Client Server


And then, run the server and client app.

```shell script
# run api server
$ cd browser-server
$ python app.py \
    --img_dir_path "../data/my-images-001" \
    --clustering_output_path "../data/clutering-results/my-images-001-clustering"

# and then run client server
$ cd ../browser-react
$ yarn start
```

Now you can browse the clustered images at [`http://localhost:3000/browser/`](`http://localhost:3000/browser/`).

## Used Libraries

- [React](https://reactjs.org/)
- [Flask](https://palletsprojects.com/p/flask/)
