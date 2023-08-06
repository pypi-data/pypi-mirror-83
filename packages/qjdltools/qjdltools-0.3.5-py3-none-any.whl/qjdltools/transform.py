# -*- coding:utf-8 -*-
'''
Data augmentations for remote sening imagery (may be with multiple bands).

Version 1.0 2019-12-06 12:36:24 by QiJi
Version 2.0 2020-08-15 10:17:19 by QiJi
'''
import cv2
import torch
import numpy as np
from qjdltools import dlimage
from PIL import Image
import torchvision.transforms as ttransform


class Resize(object):
    """
    Resize image (maybe with mask).

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.single_resize
        elif self.mode == 'seg':
            self.transform = self.join_resize

    def single_resize(self, sample):
        image = sample['image']
        if image.shape[:2] == self.insize:
            return sample

        sample['image'] = dlimage.resize_img(image, self.insize, cv2.INTER_LINEAR)
        return sample

    def join_resize(self, sample):
        image, mask = sample['image'], sample['label']
        if image.shape[:2] == self.insize:
            return sample

        h, w = self.insize

        image = dlimage.resize_img(image, self.insize, cv2.INTER_LINEAR)
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomCrop(object):
    """
    Random crop image (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.random_crop

        elif self.mode == 'seg':
            self.transform = self.random_crop_pair

    def random_crop(self, sample):
        image = sample['image']
        if (image.shape[0] > self.insize[0]) and (image.shape[1] > self.insize[1]):
            image = dlimage.random_crop(image, self.insize)
        sample['image'] = image
        return sample

    def random_crop_pair(self, sample):
        image, mask = sample['image'], sample['label']
        image, mask = dlimage.random_crop_pair(image, mask, self.insize)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class CenterCrop(object):
    """
    Center crop image (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.center_crop

        elif self.mode == 'seg':
            self.transform = self.center_crop_pair

    def center_crop(self, sample):
        image = sample['image']
        if (image.shape[0] > self.insize[0]) and (image.shape[1] > self.insize[1]):
            image = dlimage.center_crop(image, self.insize)
        sample['image'] = image
        return sample

    def center_crop_pair(self, sample):
        image, mask = sample['image'], sample['label']
        image = dlimage.center_crop(image, self.insize)
        mask = dlimage.center_crop(mask, self.insize)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomScaleAspctCrop(object):
    """
    Random crop image (maybe with mask).

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, scale=(0.25, 0.75), ratio=(3./4., 4./3.), p=0.5, mode='cls'):
        self.mode = mode
        self.insize = insize
        self.scale = scale
        self.ratio = ratio
        self.p = p

        if self.mode == 'cls':
            self.transform = self.random_scale_aspct_crop

        elif self.mode == 'seg':
            self.transform = self.join_random_scale_aspct_crop

    def random_scale_aspct_crop(self, sample):
        image = sample['image']
        if image.shape[0] < self.insize[0]:
            image = dlimage.resize_img(image, self.insize)

        H, W = image.shape[:2]  # ori_height, ori_width
        area = H*W
        if np.random.random() < self.p:
            for attempt in range(5):
                target_area = np.random.uniform(*self.scale) * area
                aspect_ratio = np.random.uniform(*self.ratio)

                w = int(round(np.sqrt(target_area * aspect_ratio)))
                h = int(round(np.sqrt(target_area / aspect_ratio)))

                if np.random.random() < 0.5:
                    w, h = h, w

                if w < W and h < H:
                    i = np.random.randint(0, H - h)  # crop start point(row/y)
                    j = np.random.randint(0, W - w)  # crop start point(col/x)
                    sample['image'] = dlimage.resized_crop(
                        image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
                    return sample
        else:
            w, h = W, H
        # Fallback
        w, h = min(w, W), min(h, H)
        i, j = (H - w) // 2, (W - w) // 2
        sample['image'] = dlimage.resized_crop(
            image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
        return sample

    def join_random_scale_aspct_crop(self, sample):
        image, mask = sample['image'], sample['label']

        H, W = image.shape[:2]  # ori_height, ori_width
        area = H*W
        if np.random.random() < self.p:
            for attempt in range(3):
                target_area = np.random.uniform(*self.scale) * area
                aspect_ratio = np.random.uniform(*self.ratio)

                w = int(round(np.sqrt(target_area * aspect_ratio)))
                h = int(round(np.sqrt(target_area / aspect_ratio)))

                if np.random.random() < 0.5:
                    w, h = h, w

                if w < W and h < H:
                    i = np.random.randint(0, H - h)  # crop start point(row/y)
                    j = np.random.randint(0, W - w)  # crop start point(col/x)
                    sample['image'] = dlimage.resized_crop(
                        image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
                    sample['label'] = dlimage.resized_crop(
                        mask, i, j, h, w, self.insize, cv2.INTER_NEAREST)
                    return sample
        else:
            w, h = W, H
        # Fallback
        w, h = min(w, W), min(h, H)
        i, j = (H - w) // 2, (W - w) // 2
        sample['image'] = dlimage.resized_crop(
            image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
        sample['label'] = dlimage.resized_crop(
            mask, i, j, h, w, self.insize, cv2.INTER_NEAREST)
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class SpaceAugment(object):
    """
    Space data augmentations for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self,
                 shift_limit=(-0.0, 0.0),
                 scale_limit=(-0.0, 0.0),
                 rotate_limit=(-0.0, 0.0),
                 aspect_limit=(-0.0, 0.0),
                 rot=True,
                 flip=True,
                 p=0.5,
                 mode='cls'):
        self.mode = mode
        self.shift_limit = shift_limit
        self.scale_limit = scale_limit
        self.rotate_limit = rotate_limit
        self.aspect_limit = aspect_limit
        self.if_rot = rot
        self.if_flip = flip
        self.p = p

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        image, mask = sample['image'], sample['label']

        # Join Random Filp
        if self.if_flip:
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image, mask = dlimage.filp_array(image, f), dlimage.filp_array(mask, f)

        # Join Random Roate (Only 0, 90, 180, 270)
        if self.if_rot:
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise
            mask = np.rot90(mask, k, (1, 0))

        # Affine transformation
        image, mask = dlimage.randomShiftScaleRotate(
            image, mask,
            shift_limit=self.shift_limit, scale_limit=self.scale_limit,
            rotate_limit=self.rotate_limit, aspect_limit=self.aspect_limit,
            # borderMode=cv2.BORDER_REFLECT,
            p=self.p)

        sample['image'], sample['label'] = image, mask
        return sample

    def single_transform(self, sample):
        image = sample['image']

        # Join Random Filp
        if self.if_flip:
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image = dlimage.filp_array(image, f)

        # Random Roate (Only 0, 90, 180, 270)
        if self.if_rot:
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise

        # Affine transformation
        image = dlimage.randomShiftScaleRotate(
            image,
            shift_limit=self.shift_limit, scale_limit=self.scale_limit,
            rotate_limit=self.rotate_limit, aspect_limit=self.aspect_limit,
            # borderMode=cv2.BORDER_REFLECT,
            p=self.p)

        sample['image'] = image
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomRotateAndFlip(object):
    """
    Random rotate for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, p=0.5, mode='cls'):
        self.mode = mode
        self.p = p

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        if np.random.random() < self.p:
            image, mask = sample['image'], sample['label']

            # Join Random Filp
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image, mask = dlimage.filp_array(image, f), dlimage.filp_array(mask, f)

            # Join Random Roate (Only 0, 90, 180, 270)
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise
            mask = np.rot90(mask, k, (1, 0))

            sample['image'], sample['label'] = image, mask
        return sample

    def single_transform(self, sample):
        if np.random.random() < self.p:
            image = sample['image']

            # Join Random Filp
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image = dlimage.filp_array(image, f)

            # Random Roate (Only 0, 90, 180, 270)
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise

            sample['image'] = image
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class ColorAugment(object):
    """ ColorJitter data augmentations for ndarray image sized of (H, W, C).
    support single- or multi- band(s) imagery.

    Args:
        dtype: `RGB` or `other`
    Note:
        For RGB imagery, jitter 'hue', 'sat' and 'val', 'contrast' according to
            `hue_shift_limit`, `sat_shift_limit`, `val_shift_limit`, 'contrast', respectively.

        For other type imagery, jitter brightness and contrast of each band,
            according to `brightness` and `contrast`, respectively.
    """
    def __init__(self,
                 hue=0,
                 sat=0,
                 brightness=0,
                 contrast=0,
                 p=0.5,
                 dtype='RGB'):
        self.p = p

        if dtype == 'RGB':
            self.ColorJitter = ttransform.Compose([ttransform.ColorJitter(
                brightness, contrast, sat, hue)])
            self.transform = self.rgb_transform
        else:
            self.brightness = brightness / 2
            self.contrast = contrast / 2
            self.transform = self.other_transform

    def rgb_transform(self, sample):
        if np.random.random() < self.p:
            image = Image.fromarray(sample['image'], 'RGB')
            image = np.asarray(self.ColorJitter(image))
            sample['image'] = image
        return sample

    def other_transform(self, sample):
        if np.random.random() < self.p:
            image = sample['image']

            if len(image.shape) == 2:
                image = image[:, :, np.newaxis]
                image = dlimage.randomColorAugment(
                    image, self.brightness, self.contrast)
            elif len(image.shape) == 3:
                band_num = image.shape[2]
                for c in range(0, band_num):
                    image[:, :, c] = dlimage.randomColorAugment(
                        image[:, :, c], self.brightness, self.contrast)
            else:
                raise TypeError("image and label should be [HW] or [HWC]")

            sample['image'] = image

        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomBlur(object):
    """ Randomly blur image sized of [HW] or [HWC],
    support single- or multi- band(s) imagery.

    Args:
        ksize: (int) the kernel size
        type: (str) the type of blur
        p: (float) Probability of diverse noises being applied.
    """
    def __init__(self, ksize=3, ktype='mean', sigma=[.1, 2.], p=0.5):
        self.p = p
        self.ksize = ksize
        self.ktype = ktype
        self.sigma = sigma

        self.blur = {
            'mean': cv2.blur, 'median': cv2.medianBlur, 'gaussian': cv2.GaussianBlur
        }[ktype]
        self.kwargs = {'ksize': (self.ksize, self.ksize)}

    def __call__(self, sample):
        if np.random.random() < self.p:
            # sample['image'] = dlimage.blur(sample['image'], self.ksize)
            image = sample['image']
            if self.ktype == 'gaussian':  # TODO: too slowly
                sigma = np.random.uniform(self.sigma[0], self.sigma[1])
                self.kwargs.update({'sigmaX': sigma, 'sigmaY': sigma})
            if len(image.shape) == 2 or image.shape[2] < 4:
                image = self.blur(image, **self.kwargs)
            else:
                for c in range(image.shape[2]):
                    band = image[:, :, c]
                    image[:, :, c] = self.blur(band, **self.kwargs)
            sample['image'] = image

        return sample


class RandomNoise(object):
    """ Randomly add a kind of noise on image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        modes: (string list) a set of noise patterns that may be applied to the image,
            but only one at a time.
            - 'gaussian'  Gaussian-distributed additive noise.
            - 'localvar'  Gaussian-distributed additive noise, with specified
                        local variance at each point of `image`.
            - 'poisson'   Poisson-distributed noise generated from the data.
            - 'salt'      Replaces random pixels with 1.
            - 'pepper'    Replaces random pixels with 0 (for unsigned images) or
                        -1 (for signed images).
            - 's&p'       Replaces random pixels with either 1 or `low_val`, where
                        `low_val` is 0 for unsigned images or -1 for signed
                        images.
            - 'speckle'   Multiplicative noise using out = image + n*image, where
                        n is uniform noise with specified mean & variance.
        p: (float) Probability of diverse noises being applied.
    """
    def __init__(self, modes=['gaussian', 's&p'], p=0.5):
        self.p = p
        self.modes = modes

    def __call__(self, sample):
        if np.random.random() < self.p:
            sample['image'] = dlimage.random_noise(sample['image'], mode=np.random.choice(self.modes))

        return sample


class RandomGrayscale(object):
    """Randomly convert image to grayscale with a probability of p (default 0.1).

    Args:
        p (float): probability that image should be converted to grayscale.
        grayway (str): `mean` or `one`.
            'mean': take mean of each band.
            'one': random choice one band

        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
    """
    def __init__(self, p=0.1, grayway='mean'):
        self.p = p
        self.grayscale = {'mean': self.grayscale_mean,
                          'one': self.grayscale_one}[grayway]

    def grayscale_mean(self, image):
        band_num = image.shape[2]
        gary_img = np.mean(image, axis=2, keepdims=True).astype(np.uint8)
        image = np.repeat(gary_img, band_num, axis=2)
        return image

    def grayscale_one(self, image):
        band_num = image.shape[2]
        gray_band = np.random.randint(0, band_num)
        image = image[:, :, gray_band]
        image = np.repeat(np.expand_dims(image, axis=2), band_num, axis=2)
        return image

    def __call__(self, sample):
        image = sample['image']

        if len(image.shape) == 3:
            if np.random.random() < self.p:
                image = self.grayscale(image)
        sample['image'] = image
        return sample


class ToTensor(object):
    """ Convert `numpy.ndarray` image sized of [H,W] or [H,W,C] in the range [0, 255]
    to a torch.FloatTensor tensor of shape [C, H, W] in the range [0.0, 1.0].

    Args:
        sample
            - if sample is a dict in format of {'image': image}, return dict.
            - if sample is a numpy.ndarray, return ndarray.
    """
    def __call__(self, sample):
        if isinstance(sample, dict):
            image = sample['image']
            if len(image.shape) < 3:
                image = image[:, :, np.newaxis]
            # [H,W,C] array -> [C,H,W] tensor
            image = torch.from_numpy(image.copy().transpose((2, 0, 1)))
            image = image.float().div_(255)
            sample['image'] = image.contiguous()
        elif isinstance(sample, np.ndarray):
            if len(sample.shape) < 3:
                sample = sample[:, :, np.newaxis]
            sample = torch.from_numpy(sample.copy().transpose((2, 0, 1)))
            sample = sample.float().div_(255).contiguous()
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class ToTensor2(object):
    """ Convert image and (may be with) label to tensor.

    Args:
        sample = {'image': image, 'label': label}

    Return:
        {'image': img_tensor, 'label', lbl_tensor}, where img_tensor is a
        torch.FloatTensor of shape [C, H, W] in the range [0.0, 1.0],
        lbl_tensor a torch.LongTensor.
    """
    def __call__(self, sample):
        img = sample['image'].copy()

        if isinstance(img, np.ndarray):
            if len(img.shape) < 3:
                img = img[:, :, np.newaxis]
            # [H,W,C] array -> [C,H,W] tensor
            img = torch.from_numpy(img.copy().transpose((2, 0, 1)))
            img = img.float().div_(255)
        else:
            raise TypeError(
                "Input image should be ndarray, got {}".format(type(img)))
        sample['image'] = img

        if 'label' in sample:
            lbl = sample['label']
            if isinstance(lbl, np.ndarray):
                sample['label'] = torch.from_numpy(lbl).long()
            else:
                sample['label'] = torch.tensor(lbl).long()

        return sample


class Normalizer(object):
    """
    Normalize image which is a Tensor of size (C, H, W), C maybe more than three!

    Args:
        sample (dict): {'image': image, 'label': label},
        mean (sequence): Sequence of means for each channel (R,G,B,NIR, SAR).
        std (sequence): Sequence of standard deviations for each channely.
    """
    def __init__(self, mean, std):
        if mean is None:
            self.mean = [0.5, 0.5, 0.5]
        else:
            self.mean = mean
        if std is None:
            self.std = [0.3125, 0.3125, 0.3125]
        else:
            self.std = std

    def __call__(self, sample):
        if isinstance(sample, dict):
            for t, m, s in zip(sample['image'], self.mean, self.std):
                t.sub_(m).div_(s)
        elif isinstance(sample, np.ndarray):
            for t, m, s in zip(sample, self.mean, self.std):
                # t.sub_(m).div_(s)
                raise NotImplementedError
        elif isinstance(sample, torch.Tensor):
            for t, m, s in zip(sample, self.mean, self.std):
                t.sub_(m).div_(s)
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class UnNormalizer(object):
    """
    UnNormalize image which is a Tensor of size (C, H, W), C maybe more than three!

    Args:
        sample (dict): {'image': image, 'label': label},
    """
    def __init__(self, mean=None, std=None):
        if mean is None:
            self.mean = [0.5, 0.5, 0.5]
        else:
            self.mean = mean
        if std is None:
            self.std = [0.3125, 0.3125, 0.3125]
        else:
            self.std = std

    def __call__(self, sample):
        if isinstance(sample, dict):
            for t, m, s in zip(sample['image'], self.mean, self.std):
                t.mul_(s).add_(m)
        elif isinstance(sample, np.ndarray):
            for t, m, s in zip(sample, self.mean, self.std):
                # t.sub_(m).div_(s)
                raise NotImplementedError
        elif isinstance(sample, torch.Tensor):
            for t, m, s in zip(sample, self.mean, self.std):
                t.mul_(s).add_(m)
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class RotateAndFlip(object):
    """
    Rotate for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        flip_code:  -2-no_flip, 0-left/right, 1-up/down, -1 left/right & up/down
        rot_code: 0-no_rot, 1-90, 2-180, 3-270
    """
    def __init__(self, rot_code=0, flip_code=-2, mode='cls'):
        self.mode = mode
        self.rot_code = rot_code
        self.flip_code = flip_code

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        image, mask = sample['image'], sample['label']

        # Join Random Filp
        if self.flip_code != -2:
            image = dlimage.filp_array(image, self.flip_code)
            mask = dlimage.filp_array(mask, self.flip_code)

        # Join Random Roate (Only 0, 90, 180, 270)
        image = np.rot90(image, self.rot_code, (1, 0))  # clockwise
        mask = np.rot90(mask, self.rot_code, (1, 0))

        sample['image'], sample['label'] = image, mask

        return sample

    def single_transform(self, sample):
        image = sample['image']

        if self.flip_code != -2:
            image = dlimage.filp_array(image, self.flip_code)

        # Random Roate (Only 0, 90, 180, 270)
        image = np.rot90(image, self.rot_code, (1, 0))  # clockwise

        sample['image'] = image
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class Shift(object):
    """
    Shift image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        shift_code: (Row_shft, Col_shift)
    """
    def __init__(self, shift_code=(0, 0), mode='cls'):
        self.mode = mode
        self.shift_code = shift_code

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        raise NotImplementedError
        return sample

    def single_transform(self, sample):
        image = sample['image']

        H, W = image.shape[:2]
        dim = len(image.shape)

        pad_params = [(0, 0)] * dim
        # Row_shft
        dy = int(H * self.shift_code[0])
        if dy < 0:
            image = image[:H+dy, :]
            pad_params[0] = (0, -dy)
        elif dy > 0:
            image = image[dy:, :]
            pad_params[0] = (dy, 0)

        dx = int(W * self.shift_code[1])
        if dx < 0:
            image = image[:, :W+dx]
            pad_params[1] = (0, -dx)
        elif dx > 0:
            image = image[:, dx:]
            pad_params[1] = (dx, 0)

        sample['image'] = np.pad(image, pad_params, 'constant')
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class Grayscale(object):
    """Convert image to grayscale.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        p (float): probability that image should be converted to grayscale.

    Returns:
        ndarray: Grayscale version of the input image with probability p and unchanged
        with probability (1-p).
        - If input image is 1 channel: grayscale version is 1 channel
        - If input image is multi- channel: grayscale version is random single channel
            of input image and return the output image with same shape as input image.

    """
    def __init__(self, band=None):
        self.band = band

    def __call__(self, sample):
        image = sample['image']

        if len(image.shape) == 3:
            band_num = image.shape[2]
            if (self.band is not None) and (self.band < band_num):
                gray_img = image[:, :, self.band]
                image = np.expand_dims(gray_img, axis=2)
            else:
                gary_img = np.mean(image, axis=2, keepdims=True).astype(np.uint8)
            image = np.repeat(gary_img, band_num, axis=2)
        sample['image'] = image
        return sample


def unnormalize(tensor, mean, std, to_array=False, pil=False):
    ''' Input [NCHW] tensor'''
    if len(tensor.shape) == 2:
        tensor = tensor[None, None, :]
    elif len(tensor.shape) == 3:
        tensor = tensor.unsqueeze(dim=0)
    for n in range(tensor.shape[0]):
        for t, m, s in zip(tensor[n, :], mean, std):
            t.mul_(s).add_(m)

    if to_array:
        array = (tensor * 255).permute(0, 2, 3, 1).cpu().numpy().astype(np.uint8)
        if pil:
            return Image(array, 'RGB')
        return array
    return tensor


def test():
    import matplotlib.pyplot as plt
    from torchvision.transforms import Compose
    import torchvision.transforms as tt
    import PIL

    # Do test here
    img_path = 'utils/example/ex_1.jpg'
    # lbl_path = r'example/P0170.txt'
    img = cv2.imread(img_path)[:, :, ::-1]
    # pil_img = PIL.Image.fromarray(img)
    # img = cv2.imread(img_path)
    # lbl = cv2.imread(lbl_path)

    # sample = {'image': img}
    tap = [1, 1, 1, 1, 1, 1, 1, 1, ]
    input_size = (224, 224)
    transforms_list = [
        # RandomScaleAspctCrop(input_size, scale=(.3, 1.), p=tap[0], mode='cls'),
        # RandomRotateAndFlip(p=tap[1], mode='cls'),
        RandomScaleAspctCrop(input_size, scale=(.3, 1.), p=tap[0], mode='cls'),
        RandomRotateAndFlip(p=tap[1], mode='cls'),
        ColorAugment(hue=0.1, sat=0.2, brightness=0.2, contrast=0.2, p=tap[2], dtype='RGB'),
        RandomNoise(['gaussian', 'localvar', 's&p', 'speckle'], p=tap[3]),
        RandomGrayscale(p=tap[4]),
        RandomBlur(3, 'mean', p=tap[5]),
        CenterCrop((100, 100))
        # RandomNoise(['gaussian', 'localvar', 's&p', 'speckle'], p=tap[3]),
        # RandomGrayscale(p=tap[4]),
        # RandomBlur(3, 'gaussian', p=tap[5]),
    ]
    # trans_1 = Compose([
    #     ColorAugment(hue=0., sat=0.8, brightness=0., contrast=0., p=1, dtype='RGB')])
    # trans_1 = Compose([
    #     SpaceAugment(mode='cls', shift_limit=(-0, 0), scale_limit=(-0.0, 0.8),
    #                  aspect_limit=(-0, 0), rotate_limit=(-0, 0), p=1)])
    # trans_2 = Compose([
    #     tt.ColorJitter(brightness=0.0, contrast=0.0, saturation=0.8, hue=0.)])
    # transforms =

    plt.figure(figsize=(9, 9), dpi=200)
    r = 3
    c = 3
    plt.subplot(r, c, 1)
    plt.imshow(img)
    plt.title('Org')
    plt.axis("off")
    # cv2.imshow('Org', img)

    # plt.subplot(r, c, 2)
    # img1 = trans_1({'image': img})['image']
    # plt.imshow(img1)
    # plt.title(str(2))
    # plt.axis("off")
    # plt.subplot(r, c, 3)
    # plt.imshow(trans_2(pil_img))
    # plt.title(str(3))
    # plt.axis("off")

    for i, trans in enumerate(transforms_list):
        plt.subplot(r, c, i+2)
        img = Compose([trans])({'image': img})['image']
        # cv2.imshow('%d' % i, img)
        plt.imshow(img)
        plt.title(str(i+2))
        plt.axis("off")
    plt.show()
    # cv2.waitKey(0)

    # def plotnoise(img, mode, r, c, i):
    #     plt.subplot(r, c, i)
    #     if mode is not None:
    #         gimg = dlimage.random_noise(img, mode=mode)
    #         plt.imshow(gimg)
    #     else:
    #         plt.imshow(img)
    #     plt.title(mode)
    #     plt.axis("off")

    # plt.figure(figsize=(18, 24))
    # r = 4
    # c = 2
    # plotnoise(img, "gaussian", r, c, 1)
    # plotnoise(img, "localvar", r, c, 2)
    # plotnoise(img, "poisson", r, c, 3)
    # plotnoise(img, "salt", r, c, 4)
    # plotnoise(img, "pepper", r, c, 5)
    # plotnoise(img, "s&p", r, c, 6)
    # plotnoise(img, "speckle", r, c, 7)
    # plotnoise(img, None, r, c, 8)
    # plt.show()

    # Show result and self check

    pass


def demo():
    import matplotlib.pyplot as plt

    img_path = 'utils/example/ex_1.jpg'
    img = cv2.imread(img_path)[:, :, ::-1]

    plt.figure(figsize=(9, 9), dpi=200)
    r = 2
    c = 5
    # brightness
    for i, brightness_factor in enumerate([0.5, 0.8, 1, 1.2, 1.5]):
        plt.subplot(r, c, i + 1)
        image = img.copy()
        if brightness_factor > 1:
            alpha = brightness_factor - 1
            degenerate = np.ones_like(img[:, :, 1]) * 255
        elif brightness_factor <= 1:
            alpha = 1 - brightness_factor
            degenerate = np.zeros_like(img[:, :, 1])
        image[:, :, 1] = cv2.addWeighted(degenerate, alpha, image[:, :, 1],
                                         (1 - alpha), 0)
        # cv2.imshow('%d' % i, img)
        plt.imshow(image)
        plt.title('%.2f' % brightness_factor)
        plt.axis("off")

    # contrast
    for i, contrast_factor in enumerate([0.5, 0.8, 1, 1.2, 1.5]):
        plt.subplot(r, c, c + i + 1)
        image = img.copy()
        image[:, :, 1] = np.clip(image[:, :, 1] * contrast_factor, 0,
                                 255).astype(np.uint8)
        # cv2.imshow('%d' % i, img)
        plt.imshow(image)
        plt.title('%.2f' % contrast_factor)
        plt.axis("off")
    plt.show()


if __name__ == "__main__":
    # test()
    demo()
    pass
