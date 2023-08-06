from PIL import Image
import os
import os.path
import numpy as np
import sys

if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_url, check_integrity


class GripCifar10(VisionDataset):

    base_folder = 'cifar10'
    url = None
    filename = None
    tgz_md5 = None
    train_list = [['data_batch', None]]

    test_list = [['test_batch', None]]
    meta = {
        'filename': 'batches.meta',
        'key': 'label_names',
        'md5': None,
    }

    # db_mean = (0.61799215, 0.29761591, 0.37573633, 0.52014014)#(0.60075633,0.30408495, 0.37778071, 0.22482509)
    # db_std = (0.10109334, 0.1636474, 0.14329318, 0.0625928)#(0.11525005,0.2022998,  0.17382977, 0.09038225)

    # db_mean = (0.60754877, 0.38245198, 0.44624274, 0.43154834)
    # db_std = (0.14569339, 0.18942552, 0.17363705, 0.02090128)

    # db_mean = (0.42988802, 0.42988802, 0.42988802)    #grip_evaluator_depth_20200327
    # db_std = (0.02043479, 0.02043479, 0.02043479)

    # db_mean = (0.60747145, 0.3981848,  0.45978323)    # grip_evaluator_rgb_20200327
    # db_std = (0.14146864, 0.18522996, 0.17041358)

    # db_mean = (0.55005549, 0.55005549, 0.55005549)      # grip_evaluator_depth_20200329
    # db_std = (0.03288065, 0.03288065, 0.03288065)

    # db_mean = (0.55184516, 0.55184516, 0.55184516)      # grip_evaluator_depth_20200408
    # db_std = (0.03759594, 0.03759594, 0.03759594)

    # db_mean = (0.54323941, 0.54323941, 0.54323941)  # grip_evaluator_depth_20200409
    # db_std = (0.04577378, 0.04577378, 0.04577378)

    # db_mean = (0.54602665, 0.54602665, 0.54602665)  # grip_evaluator_depth_20200423
    # db_std = (0.03714684, 0.03714684, 0.03714684)

    # db_mean = (0.35978138, 0.41708053, 0.5188343,  0.53351979)  # grip_evaluator_depth_20200424
    # db_std = (0.11914077, 0.10032271, 0.12174645, 0.04099747)

    # db_mean = (0.33610585, 0.38967911, 0.49009963, 0.52970528)  # grip_evaluator_depth_20200427
    # db_std = (0.12106411, 0.10579008, 0.12965363, 0.04399332)

    # db_mean = (0.42963929 0.44455258 0.42168464 0.50111799)  # 20200512, or use 202200427
    # db_std = (0.145406   0.137699   0.1424108  0.03611386)

    # db_mean = (0.41280124, 0.42837454, 0.42626716, 0.31356105)  # 20200514
    # db_std = (0.15362443, 0.15150588, 0.15615994, 0.03650546)

    # db_mean = (0.36361247, 0.40355713, 0.46720627, 0.45218567)  # 20200518
    # db_std = (0.13274179, 0.12218594, 0.13916006, 0.04130782)

    # db_mean = (0.76513104, 0.74994571, 0.74697943, 0.4860831)  # 20200610
    # db_std = (0.17024282, 0.1789022,  0.1872297,  0.09504798)

    db_mean = (0.41828456, 0.40237707, 0.41067797, 0.24735339, 0.1663269,  0.85723261)  # 20200624
    db_std = (0.14510322, 0.14341601, 0.14637822, 0.25664706, 0.21761108, 0.16026509)

    def __init__(self, root=None, train=True,
                 transform=None, target_transform=None,
                 download=False, im_shape=(32, 32, 3), data=None, indexing=False):

        super(GripCifar10, self).__init__(root)
        self.transform = transform
        self.target_transform = target_transform

        self.indexing = indexing

        self.train = train  # training set or test set
        if download:
            self.download()

        if data is None:
            if not self._check_integrity():
                raise RuntimeError('Dataset not found or corrupted.' +
                                   ' You can use download=True to download it')

        if self.train:
            downloaded_list = self.train_list
        else:
            downloaded_list = self.test_list

        self.data = []
        self.targets = []
        if data is not None: self.targets = [0] * len(data)
        if data is None:
            # now load the picked numpy arrays
            for file_name, checksum in downloaded_list:
                file_path = os.path.join(self.root, self.base_folder, file_name)
                with open(file_path, 'rb') as f:
                    if sys.version_info[0] == 2:
                        entry = pickle.load(f)
                    else:
                        # entry = pickle.load(f, encoding='latin1')
                        entry = pickle.load(f)
                    self.data.append(entry['data'])
                    if 'labels' in entry:
                        self.targets.extend(entry['labels'])
                    else:
                        self.targets.extend(entry['fine_labels'])

            self._load_meta()
            self.data = np.vstack(self.data).reshape(-1, im_shape[2], im_shape[0], im_shape[1])
            self.data = self.data.transpose((0, 2, 3, 1))  # convert to HWC
        else:
            self.data = np.vstack([p.reshape((1,) + p.shape) for p in data])


    def array2cifar(self, anArray):
        h, w, ch = anArray.shape
        out = [anArray[:, :, i].reshape(1, h * w) for i in range(ch)]
        return np.hstack(out)

    def _load_meta(self):
        path = os.path.join(self.root, self.base_folder, self.meta['filename'])
        if not check_integrity(path, self.meta['md5']):
            raise RuntimeError('Dataset metadata file not found or corrupted.' +
                               ' You can use download=True to download it')
        with open(path, 'rb') as infile:
            if sys.version_info[0] == 2:
                data = pickle.load(infile)
            else:
                data = pickle.load(infile, encoding='latin1')
            self.classes = data[self.meta['key']]
        self.class_to_idx = {_class: i for i, _class in enumerate(self.classes)}

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[index], self.targets[index]

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        # img = Image.fromarray(img)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)
        if self.indexing:
            return img, target, index
        else:
            return img, target

    def __len__(self):
        return len(self.data)

    def _check_integrity(self):
        root = self.root
        for fentry in (self.train_list + self.test_list):
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    def download(self):
        import tarfile

        if self._check_integrity():
            print('Files already downloaded and verified')
            return

        download_url(self.url, self.root, self.filename, self.tgz_md5)

        # extract file
        with tarfile.open(os.path.join(self.root, self.filename), "r:gz") as tar:
            tar.extractall(path=self.root)

    def extra_repr(self):
        return "Split: {}".format("Train" if self.train is True else "Test")

