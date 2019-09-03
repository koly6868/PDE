from PIL import Image
import numpy as np
import imageio

def ImageToNdarray(path:str):
    img = Image.open(path)
    ary = np.array(img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)

    # Standard RGB to grayscale 
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], 
    zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)

    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save('road.bmp')
    return bitmap

def SaveArrayAsImage(path : str, arr : np.ndarray):
    im = Image.fromarray(arr.astype(np.uint8))
    im.save(path)

def ImagesToGif(filenames, gif_path):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(gif_path + r"/solution.gif", images)

if __name__ == "__main__":
    images_path = r"solution/"
    np.load("result.npy")


