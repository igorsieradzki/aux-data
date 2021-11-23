import numpy as np
import os
from datasets.dataset_config import _BASE_DATA_PATH


class AuxiliaryDataset():

    def __init__(self):

        self.fname = './data/aux.npz'
        self.data = np.load(self.fname)['arr_0']
        np.random.shuffle(self.data)
        self.beg = 0

    def get_data(self, data=None, targets=None, n_samples=None):

        end = self.beg + n_samples

        if end > len(self.data):
            self.beg = 0
            end = n_samples

        output = self.data[self.beg: end]
        self.beg = end

        return np.transpose(output, (0, 2, 3, 1))


class AuxDatasetIN():

    def __init__(self):
        self.excluded_classes = {68, 56, 78, 8, 23, 84, 90, 65, 74, 76, 40, 89, 3, 92, 55, 9, 26, 80, 43, 38, 58, 70,
                                 77, 1, 85, 19, 17, 50,
                                 28, 53, 13, 81, 45, 82, 6, 59, 83, 16, 15, 44, 91, 41, 72, 60, 79, 52, 20, 10, 31, 54,
                                 37, 95, 14, 71, 96,
                                 98, 97, 2, 64, 66, 42, 22, 35, 86, 24, 34, 87, 21, 99, 0, 88, 27, 18, 94, 11, 12, 47,
                                 25, 30, 46, 62, 69,
                                 36, 61, 7, 63, 75, 5, 32, 4, 51, 48, 73, 93, 39, 67, 29, 49, 57, 33}

        self.data = []
        self.beg = 0

        path = os.path.join(_BASE_DATA_PATH, 'ILSVRC12_256')
        trn_lines = np.loadtxt(os.path.join(path, 'train.txt'), dtype='U200')

        for image, label in trn_lines:
            if not os.path.isabs(image):
                image = os.path.join(path, image)
            label = int(label)
            if label not in self.excluded_classes:
                self.data.append(image)

        np.random.shuffle(self.data)

    def get_data(self, data=None, targets=None, n_samples=None):

        end = self.beg + n_samples

        if end > len(self.data):
            self.beg = 0
            end = n_samples

        output = self.data[self.beg:end]
        self.beg = end

        return output


neg_data = AuxiliaryDataset()
in_data = AuxDatasetIN()

aux_loaders = {'ti': neg_data.get_data,
               'in': in_data.get_data}


