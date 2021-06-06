import torch
from torch.utils.data.dataset import Dataset
from torchvision import transforms
from PIL import Image
from utils.processing import *

class PilotNetDataset(Dataset):
    def __init__(self, path_to_data, path_to_data_curve, horizon, transforms=None):

        self.data_path = path_to_data
        self.horizon = horizon

        all_images, all_data = load_data(path_to_data)
        all_images_curve, all_data_curve = load_data(path_to_data_curve)

        type_image = 'cropped'

        self.images = []
        self.images = get_images(all_images, type_image, self.images)
        # self.images = get_images(all_images_curve, type_image, self.images)

        self.labels = []
        self.labels = parse_json(all_data, self.labels)
        # self.labels = parse_json(all_data_curve, self.labels)

        self.labels, self.images = preprocess_data(self.labels, self.images)

        self.transforms = transforms

        self.image_shape = self.images[0].shape
        self.num_labels = np.array(self.labels[0]).shape[0]

        self.count = len(self.images)
        
    def __getitem__(self, index):

        index = np.clip(index,0,self.count-self.horizon)

        all_imgs = []

        for iter in range(4):
            img = self.images[index+iter]
            label = np.array(self.labels[index])
            data = Image.fromarray(img)

            if self.transforms is not None:
                data = self.transforms(data)

            all_imgs.append(data)
            
        set_data = torch.vstack(all_imgs)

        return (set_data, label)

    def __len__(self):
        return self.count