from torch.utils.data.dataset import Dataset
from torchvision import transforms
from PIL import Image
from utils.processing import *

class DeepPilotDataset(Dataset):
    def __init__(self, path_to_data, mode='train', transforms=None):

        self.data_path = path_to_data

        if mode == 'train':
            datatset = getTrainSource(self.data_path + 'train/')
        elif mode == 'test':
            datatset = getTestSource(self.data_path + 'test/')
        else:
            assert False, 'Mode should be train/test'

        self.images = datatset.images
        self.labels = datatset.speed

        self.transforms = transforms

        self.image_shape = self.images[0].squeeze().shape
        self.num_labels = np.array(self.labels[0]).shape[0]

        self.count = len(self.images)
        
    def __getitem__(self, index):

        img = self.images[index]
        label = np.array(self.labels[index])

        data = Image.fromarray(img.squeeze())

        if self.transforms is not None:
            data = self.transforms(data)

        return (data, label)

    def __len__(self):
        return self.count