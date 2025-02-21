import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from PIL import Image
import os
import shutil

img_dir = "tshirt"
output_dir =  os.path.join(img_dir, "output")
pca_num = 10

def reduce_pca(n_components, in_arr):
    # Reduce the dimensions with PCA
    pca = PCA(n_components=n_components)
    return pca.fit_transform(in_arr)

def convert_img_to_gray(img_path):
    # Open an image and convert it to an array
    image = Image.open(img_path).resize([516, 655]).convert("RGB")
    img_arr = np.array(image)
    # Convert to grayscale
    gray_arr = 0.2989 * img_arr[:, :, 0] + 0.5870 * img_arr[:, :, 1] + 0.1140 * img_arr[:, :, 2]
    return gray_arr.flatten()  # Flatten to 1D array

def load_images(img_dir):
    image_data = []
    file_names = []
    # For every image in the given folder
    for img in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img)
        if os.path.isfile(img_path):
            try:
                gray_img = convert_img_to_gray(img_path)
                # Add it to array which contains images flatten grayscale pixels
                image_data.append(gray_img)
                # Add image name to a seperate array
                file_names.append(img)
            except Exception as e:
                print(f"Error processing {img}: {e}")

    # Apply PCA to reduce dimensions
    image_data = np.array(image_data)

    reduced_data = reduce_pca(pca_num, image_data)
    reduced_data = image_data

    # Concat image names to their reduced data
    return np.hstack([np.array(file_names).reshape(-1, 1), reduced_data])

def clustering(images_arr, n_clusters : int, optimizaing : bool = False):
    # Apply Kmeans for clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    features = images_arr[:, 1:].astype(float)  # Convert features to float
    labels = kmeans.fit_predict(features)

    # In optimizing mode there is no need to save images 
    if not optimizaing:
        # Organize images into clusters
        for cls in np.unique(labels):
            # Create a folder for every cluster
            cls_folder = os.path.join(output_dir, str(cls))
            os.mkdir(cls_folder)
            # Filter images of that cluster
            cls_images = images_arr[labels == cls, 0]
            # Copy all images of the cluster into related folder
            for img_name in cls_images:
                shutil.copyfile(os.path.join(img_dir, img_name), os.path.join(cls_folder, img_name))
            
        # Plotting the clusters based on first two features
        plot_clusters(features, labels)

    return features, labels, kmeans.inertia_


def optimize_clustering(images_arr):
     #elbow method
    inertias = []
    iterations = 10 # which cluster number to examine
    for i in range(1, iterations+1):
        # perform clustering to discover the inertia for every cluster number
        features, cluster_labels, inertia = clustering(images_arr, n_clusters=i, optimizaing=True)
        # append inertia to a list
        inertias.append(inertia)
    

    #silhouette_score metric
    silhouette_scores = []
    for i in range(2,iterations+1):
        # extract clustering characteristics for every cluster number
        features, cluster_labels, inertia = clustering(images_arr, n_clusters=i, optimizaing=True)
        # calculate silhouette_score based on clustering outputs
        silhouette_scores.append(silhouette_score(features, cluster_labels))


    # set the figure resolution and dpi
    fig = plt.figure(figsize=(16, 9), dpi=600)
    # sub plot of elbow method
    plt.subplot(121)
    plt.plot(range(1,iterations+1), inertias, marker = "o")
    plt.grid(True)
    plt.title("elbow method")
    plt.xlabel("cluster number")
    plt.ylabel("inertia")
    # sub plot of silhouette_scores
    plt.subplot(122)
    plt.plot(range(2,iterations+1), silhouette_scores, marker="o", c="red")
    plt.grid(True)
    plt.title("silhouette_scores")
    plt.xlabel("cluster number")
    plt.ylabel("silhouette_score")
    # save the png file of plots 
    plt.savefig(fname=  os.path.join(output_dir, "optimization.png"), format="png", dpi = fig.dpi)


def plot_clusters(features, labels):
    plt.figure(figsize=(10, 6))
    plt.scatter(features[:, 0], features[:, 1], c=labels, cmap='viridis', s=10)
    plt.title("Cluster Visualization")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.savefig(os.path.join(output_dir, "cluster_visualization.png"))

def main():
    # Load the images
    images_arr = load_images(img_dir)

    # Create output folder if needed
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    # Oprimize cluster numbes
    optimize_clustering(images_arr)

    # Cluster with optimized number and get the clustered images
    clustering(images_arr, 6)

    print("Clustering Finished!")

if __name__ == "__main__":
    main()
