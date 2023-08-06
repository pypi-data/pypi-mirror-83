from PIL import Image
import os
import os.path
import numpy as np
import sys
import torchvision.transforms as transforms
from ttcv.import_basic_utils import *

if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_url, check_integrity


class SuctionCifar10(VisionDataset):

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

    # db_mean = (0.37333256, 0.50367485, 0.6492233, 0.56081723)  # 20200511
    # db_std = (0.0414015, 0.03815473, 0.04328673, 0.01134201)

    # db_mean = (0.43503931, 0.44019999, 0.41939172, 0.55336628)  # 20200512
    # db_std = (0.06111116, 0.06243232, 0.06333934, 0.01970969)

    # db_mean = (0.39287165, 0.4465874,  0.40430869, 0.54449114)  # 20200512
    # db_std = (0.07679449, 0.07307834, 0.07486557, 0.02271312)

    # db_mean = (0.39583588, 0.4751535,  0.4489659,  0.39239821)  # 20200514
    # db_std = (0.09845068, 0.08866881, 0.08950291, 0.02083357)

    # db_mean = (0.61325816, 0.63284441, 0.62099887, 0.3794783)  # 20200521
    # db_std = (0.10611203, 0.10823587, 0.10509778, 0.02259126)

    # db_mean = (0.60783364, 0.62808136, 0.61624238, 0.38024026)  # 20200521_RB_best , (100, 60000)
    # db_std = (0.11982953, 0.11713887, 0.11431467, 0.02293329)

    # db_mean = (0.60783364, 0.62808136, 0.61624238)  # 20200521_v2 only rgb
    # db_std = (0.11982953, 0.11713887, 0.11431467)

    # db_mean = (0.41312494, 0.33027523, 0.262142,   0.6117158)  # 20200525_CH robot env
    # db_std = (0.08633106, 0.09178339, 0.10141662, 0.03975779)

    # db_mean = (0.51066111, 0.47836661, 0.43790377, 0.49762565)  # 20200525_RB_CH robot env
    # db_std = (0.0961087,  0.09922036, 0.1026221,  0.03070719)

    # db_mean = (0.60783364, 0.62808136, 0.61624238, 0.41772863)  # 20200527_RB_good
    # db_std = (0.11982953, 0.11713887, 0.11431467, 0.02475438)

    # db_mean = (0.6100014,  0.62563852, 0.60814321, 0.41632976)  # 20200527_RB_cmb_0519_0526
    # db_std = (0.11946112, 0.11505818, 0.11240116, 0.02360522)

    # db_mean = (0.50895616, 0.4740457,  0.4305609,  0.5415007)  # 20200527_RB_CH_cmb_0519_0522_0526
    # db_std = (0.10245739, 0.10311258, 0.10676344, 0.03361819)

    # db_mean = (0.49576933, 0.49576513, 0.49576391, 0.51792066)  # 20200604_RB_CH_cmb_0519_0522_0526 (fg, bound, bg)
    # db_std = (0.11185922, 0.11186486, 0.11187794, 0.03231334)

    # db_mean = (0.56726268, 0.56723482, 0.56719619, 0.47881223)  # 20200604_RB_CH_cmb_0519_0522_0526 (fg, bound)
    # db_std = (0.13903961, 0.13904731, 0.13908207, 0.03555515)

    db_mean = (0.55789759, 0.55786037, 0.55780825, 0.48949334)  # 20200608_RB_CH_cmb_0519_0522_0526_0604_0605 (fg, bound)
    db_std = (0.13491044, 0.13492254, 0.13494867, 0.03607968)

    # db_mean = (0.5639651,  0.56381155, 0.56385888, 0.18956837, 0.18703041, 0.88085926)  # 20200616_RB_CH_cmb_0519_0522_0526_0604_0605_norm_vec
    # db_std = (0.1361991,  0.13618944, 0.13621452, 0.19232603, 0.22332118, 0.13067493)



    def __init__(self, root=None, train=True,
                 transform=None, target_transform=None,
                 download=False, im_shape=(32,32,3), data=None, indexing=False):

        super(SuctionCifar10, self).__init__(root)
        self.transform = transform
        self.target_transform = target_transform

        self.indexing=indexing

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
        if data is not None: self.targets=[0]*len(data)
        timer = Timer()
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
            self.data = np.vstack([p.reshape((1,)+p.shape) for p in data])
            timer.pin_time('reshape')

        print(timer.pin_times_str())

    def array2cifar(self, anArray):
        h, w, ch = anArray.shape
        out = [anArray[:,:,i].reshape(1, h*w) for i in range(ch)]
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
        if self.indexing: return img, target, index
        else: return img, target

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

