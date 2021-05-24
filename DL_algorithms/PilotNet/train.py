import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader

from PilotNet.utils.processing import *

import json
import numpy as np

if __name__=="__main__":

    # Load data
    images, data = load_data('../datasets/complete_dataset')
    images_curve, data_curve = load_data('../datasets/curves_only')

    # CHANGE type_image
    type_image = 'cropped'
    #type_image='normal'

    # Preprocess images
    array_imgs = []
    array_imgs = get_images(images, type_image, array_imgs)
    array_imgs = get_images(images_curve, type_image, array_imgs)
    # Preprocess json
    array_annotations = []
    array_annotations = parse_json(data, array_annotations)
    array_annotations = parse_json(data_curve, array_annotations)


    if type_image == 'cropped':
        img_shape = (65, 160, 3)
    else:
        img_shape = (120, 160, 3)


    # Adapt the data
    array_annotations, array_imgs = preprocess_data(array_annotations, array_imgs)
    # x = x[:]


    # START NORMALIZE DATA
    array_annotations_v = []
    array_annotations_w = []

    for annotation in array_annotations:
    array_annotations_v.append(annotation[0])
    array_annotations_w.append(annotation[1])
    
    array_annotations_v = np.stack(array_annotations_v, axis=0)
    array_annotations_v = array_annotations_v.reshape(-1, 1)

    array_annotations_w = np.stack(array_annotations_w, axis=0)
    array_annotations_w = array_annotations_w.reshape(-1, 1)

    def normalize(x):
        x = np.asarray(x)
        return (x - x.min()) / (np.ptp(x))
    normalized_X = normalize(array_annotations_v)
    # normalized_Y = normalize(array_annotations_w)
    old_min = array_annotations_w.min()
    old_range = array_annotations_w.max() - old_min

    new_min = -1
    new_range = 2
    normalized_Y = [(n - old_min) / old_range * new_range + new_min for n in array_annotations_w]
    normalized_Y = np.array(normalized_Y)

    normalized_annotations = []
    for i in range(0, len(normalized_X)):
    normalized_annotations.append([normalized_X.item(i), normalized_Y.item(i)])

    normalized_annotations = np.stack(normalized_annotations, axis=0)
    array_annotations = normalized_annotations
    # END NORMALIZE DATA

    split_test_train_value = 0.30
    #images_train, images_validation, annotations_train, annotations_validation = \
    #    train_test_split(array_imgs, array_annotations, test_size=0.30, random_state=42)
    # FOR LSTMs -> suffle=False because the order of images is relevant
    images_train, images_validation, annotations_train, annotations_validation = \
        train_test_split(array_imgs, array_annotations, test_size=split_test_train_value, random_state=42, shuffle=False)
    #images_train, images_validation, annotations_train, annotations_validation = \
    #    train_test_split(array_2_images, array_annotations, test_size=0.30, random_state=42)

    # Adapt the data
    images_train = np.stack(images_train, axis=0)
    annotations_train = np.stack(annotations_train, axis=0)
    images_validation = np.stack(images_validation, axis=0)
    annotations_validation = np.stack(annotations_validation, axis=0)

    print(annotations_train[0])
    print(annotations_train.shape)

    #video = np.stack(array_imgs, axis=0)
    print(images_train.shape)
    print(images_validation.shape)