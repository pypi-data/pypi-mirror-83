import numpy as np
import os

# libraries to work with images
from skimage.io import imread
from skimage.transform import resize
from tqdm import tqdm

# print(len(os.listdir('dataset/train')))
# print(len(os.listdir('dataset/test')))



path ='dataset/train/'
class_labels = {'dog': 1, 'cat':0}


def prepare_data(path, h, w, class_labels):
    img_data =[]
    img_labels =[]
    for i in os.listdir(path):
        img= imread(path+i)
        # normalizing the pixel values
        img = img/255
        img = resize(img, output_shape=(h, w,3), mode='constant', anti_aliasing=True)
        # converting the type of pixel to float 32
        img = img.astype('float32')
        # appending the image into the list
        img_data.append(img)
        img_labels.append(class_labels[i.split('.')[0]])
    img_data = np.array(img_data)
    img_labels = np.array(img_labels)
    return img_data, img_labels 




train_x, train_y = prepare_data(path, 32, 32, class_labels)

print("X_train shape :", train_x.shape)
print("y_train shape :", train_y.shape)

np.save('dc_train_img_32.npy', train_x)
np.save('dc_train_labels_32.npy', train_y)