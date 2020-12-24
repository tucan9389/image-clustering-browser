# Image Clustering and Browsing

You can cluster bunch of images and browse it with web application. In this example, use faiss similarity and k-means clustering. And browse the clustered directories with the grid image web viewer.   

## DEMO

![browsing demo](https://user-images.githubusercontent.com/37643248/103070144-3b155780-4604-11eb-9635-dd1cf8627031.gif)

## Features

- [x] Cluster Million level images without copying images
- [x] View the result of clustering with huge number of images
- [x] Browse the directories which is made during clustering
- [x] Show and page bunch of images with grid gallery
- [ ] Support to run and show the progress of the clustering with buttons on the web 
- [ ] Show the featuremaps for each image

## Getting Started

### 1. Prepare Data

Download image data from what you want.

You can prepare any bunch of images like ImageNet, Coco, or your album on the mobile phone even though.  

### 2. Install Requirements

```shell script
$ 
```

### 3. Get featuremaps

```shell script
$ 
```

### 4. Run Clustering

```shell script
$ cd ~/clustering-and-browsing/clustering
$ python clustering-to-txt.py \
    --number_of_cluster 10 \
    --img_dir_path "../atms-datasets/conomi-images-10000" \
    --featuremap_dir_path "../atms-datasets/conomi-images-rexnetv1_2.0x-inferredfeatures-100000" \
    --clustering_output_path "../clutering-results/conomi-images-10000-clustering"
```

### 5. Run Browser API and Client Server

```shell script
# run api server
$ cd ~/clustering-and-browsing/browser-server
$ python app.py \ 
    --img_dir_path "../atms-datasets/conomi-images-10000" \
    --clustering_output_path "../clutering-results/conomi-images-10000-clustering"

# and then run client server
$ cd ~/clustering-and-browsing/browser-react
$ yarn start
```

And now you can browse the clustered images at `http://localhost:3000/browser/`.

## Used Functions

- faiss
- k-means clustering
- ReXNetV1
- React
- Flask

## Reference
