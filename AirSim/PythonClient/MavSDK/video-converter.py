import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('C:/Users/diego/OneDrive/Documentos/AirSim/2022-08-25-17-21-23/images/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('test5.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 12, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()