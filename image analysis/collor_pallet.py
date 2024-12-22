import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import os
import sys
from pprint import pprint
import pandas as pd

class image():
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.image = self.image.convert('RGB')
        self.image_array = np.array(self.image)
        self.image_pallet = self.get_pallet()
    
    def get_pallet(self):
        pallet = {}
        for row in self.image_array:
            for pixel in row:
                pixel = tuple(pixel)
                if len(pixel) == 3:
                    pixel = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
                elif len(pixel) == 4:
                    pixel = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
                    
                if pixel in pallet:
                    pallet[pixel] += 1
                else:
                    pallet[pixel] = 1
        return pallet
    
    def plot_pallet(self):
        # plots the colors in a 3 dimensional space with the color values as the axis values
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for color in self.image_pallet:
            #print(color)
            ax.scatter(color[0], color[1], color[2], s=self.image_pallet[color], marker='o',c=np.array(color)/255)
        ax.set_xlabel('Red Value')
        ax.set_ylabel('Green Value')
        ax.set_zlabel('Blue Value')
        plt.show()
        


def plot_pallet(image_pallet):
    # plots the colors in a 3 dimensional space with the color values as the axis values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for color in image_pallet:
        #pprint(color)
        ax.scatter(color[0], color[1], color[2], marker='o',c=[np.array(color, dtype=float)/255], s=0.1)
    ax.set_xlabel('Red Value')
    ax.set_ylabel('Green Value')
    ax.set_zlabel('Blue Value')
    plt.show()

def save_pallet(image_pallet, save_path):
    # saves the pallet to a csv file
    pallet = []
    for color in image_pallet:
        pallet.append([color[0], color[1], color[2], image_pallet[color]])
    pallet = pd.DataFrame(pallet, columns=['Red', 'Green', 'Blue', 'Count'])
    pallet.to_csv(save_path, index=False)

def load_pallet(load_path):
    # loads the pallet from a csv file
    pallet = pd.read_csv(load_path)
    image_pallet = {}
    for index, row in pallet.iterrows():
        image_pallet[(row['Red'], row['Green'], row['Blue'])] = row['Count']
    return image_pallet

def save_pallet_image(image_pallet, save_path):
    # saves the pallet to an image
    pallet = np.zeros((1, len(image_pallet), 3), dtype=np.uint8)
    for i, color in enumerate(image_pallet):
        pallet[0, i] = color
    cv2.imwrite(save_path, pallet)

def main():
    arguments = sys.argv[1:]
    flattened_pallet = {}
    for i in range(len(arguments)):
        arguments[i] = arguments[i].replace("\\", "/") 
    if len(arguments) == 1:
        # when the given argument is a path to a folder, the program will analyze all the images in the folder
        if os.path.isdir(arguments[0]):
            image_pallet = {}
            for file in os.listdir(arguments[0]):
                if file.endswith(".png") or file.endswith(".jpg"):
                    image_pallet[file] = image(arguments[0] + "/" + file).image_pallet
            #pprint(image_pallet)
            pallet = []
            for img_pallet in image_pallet.values():
                for color in img_pallet:
                    pallet.append(color)
            #pprint(pallet)
            flattened_pallet = {}
            for img_pallet in image_pallet.values():
                for color, count in img_pallet.items():
                    if color in flattened_pallet:
                        flattened_pallet[color] += count
                    else:
                        flattened_pallet[color] = count
        else:
            image_path = arguments[0]
            image(image_path)
            #pprint(image(image_path).image_pallet)
            image(image_path).plot_pallet()
    elif len(arguments) > 1:
        image_pallet = {}
        for image_path in arguments:
            image_pallet[image_path] = image(image_path).image_pallet
        #pprint(image_pallet)
        pallet = []
        for image_path in image_pallet:
            for color in image_pallet[image_path]:
                pallet.append(color)
        #pprint(pallet)
        flattened_pallet = {}
        for img_pallet in image_pallet.values():
            for color, count in img_pallet.items():
                if color in flattened_pallet:
                    flattened_pallet[color] += count
                else:
                    flattened_pallet[color] = count
    
    save_path = "image_pallet.csv"
    if os.path.exists(save_path):
        loaded_flattened_pallet = load_pallet(save_path)
        for color in loaded_flattened_pallet:
            if color in flattened_pallet:
                flattened_pallet[color] += loaded_flattened_pallet[color]
            else:
                flattened_pallet[color] = loaded_flattened_pallet[color]
        os.remove(save_path)


    save_pallet(flattened_pallet, save_path)
    
    save_path = "image_pallet.png"
    if os.path.exists(save_path):
        os.remove(save_path)
    save_pallet_image(flattened_pallet, save_path)
    
    
    plot_pallet(flattened_pallet)

if __name__ == '__main__':
    main()
