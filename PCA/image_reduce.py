import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from PIL import Image
import sys
import os

reduced_image_arr_path = "reduced_image_array.txt"
original_image_arr_path = "original_image_array.txt"

def reduce_pca(n_components : int, in_arr : np.array, verbose : bool=False) -> np.array:
    pca = PCA(n_components=n_components)

    # Reduce image dimensions with PC
    arr_reduced = pca.fit_transform(in_arr)
    # Take back the image in original size
    out_arr = pca.inverse_transform(arr_reduced)

    # In verbose mode some furthur information about PCA will be shown
    if verbose:
        print(f"PCA Components:\n{pca.components_}\nPCA Variance Ratios:\n{pca.explained_variance_ratio_}")

        # In verbose mode the array related to the reduced image will be also saved in a txt file
        decreased_file = open(reduced_image_arr_path, "a")
        decreased_file.write(f"{arr_reduced.shape}\n")
        decreased_file.write(np.array2string(arr_reduced,threshold=np.inf))
        decreased_file.write("\n\n")
        decreased_file.close()

    return out_arr 

def split_image_channels(img_arr : np.array):
    # Split channels of the image
    red = img_arr[:,:,0]
    green = img_arr[:,:,1]
    blue = img_arr[:,:,2]

    return red, green, blue

def save_show_images(original_img_arr : np.array, reduced_img_arr : np.array, verbose : bool = False):
    # Create an image based on the array and save it
    image_reduced = Image.fromarray(reduced_img_arr).convert("RGB")
    image_reduced.save("reduced_image.jpg")

    # In verbose mode the array related to the image will be also saved in a txt file
    if verbose:
        original_file = open(original_image_arr_path, "w")
        original_file.write(np.array2string(original_img_arr,threshold=np.inf))
        original_file.close()
    
    # The image is shown via matplotlib
    plt.subplot(1,2,1)
    plt.imshow(original_img_arr)

    plt.subplot(1,2,2)
    plt.imshow(reduced_img_arr)

    plt.tight_layout()
    plt.show()


def main():
    # Number of PCs is considered here
    num_pcs = 10

    if len(sys.argv) < 2:
        print("This program needs path of the image to reduce!")
        sys.exit(1)
    
    image_path = sys.argv[1]

    # Image is open and saved in an array 
    image = Image.open(image_path)
    img_arr = np.array(image)

    # The channels are slpitted 
    r_arr, g_arr, b_arr = split_image_channels(img_arr)

    if os.path.exists(reduced_image_arr_path):
        os.remove(reduced_image_arr_path)

    # each channel is reduced seperately
    r_arr_reduced = reduce_pca(num_pcs, r_arr,True)
    g_arr_reduced = reduce_pca(num_pcs, g_arr,True)
    b_arr_reduced = reduce_pca(num_pcs, b_arr,True)

    # The channels are gathered in one 3D array 
    img_arr_reduced = np.stack([r_arr_reduced,g_arr_reduced,b_arr_reduced], axis=2)

    # Save the image after PCA
    save_show_images(img_arr, np.clip(img_arr_reduced,0,255).astype(np.uint8), True)

if __name__ == "__main__":
    main()


