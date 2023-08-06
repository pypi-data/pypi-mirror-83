'''
Tools collection of Data(np.ndarray) processing.

Note:
    1. cv2.imwrite(image_name, image, [1, 100]),
        [1, 100] mean set [cv2.IMWRITE_JPEG_QUALITY, 100]

Version 1.0  2018-04-03 15:44:13 by QiJi
Version 1.5  2018-04-07 22:34:53 by QiJi
Version 2.0  2018-10-25 16:59:23 by QiJi
'''

import os

import cv2
# import h5py
import numpy as np
from tqdm import tqdm

# from .dldata import get_label_info
from .fileop import filelist, rename_file


# **********************************************
# ************ Image basic tools ***************
# **********************************************
def randomcolor(band=3):
    values = [np.random.randint(0, 255) for i in range(3)]
    return tuple(values)


def convert_image_type(image_dir, new_type, old_type=None):
    '''Covert image's type(may be specify the old type).
    Args:
        new_type: The target type of image conversion(such as: 'png', 'jpg').
    '''
    image_names = filelist(image_dir, True, old_type)
    for name in tqdm(image_names):
        img = cv2.imread(name, 1)  # 默认BGR模式读，适应Tiff的标签图
        os.remove(name)
        name = os.path.splitext(name)[0]+'.'+new_type
        cv2.imwrite(name, img, [1, 100])


def one_hot_1(label, class_num):
    '''One hot code the label, not support RBG label.
    Args:
        label: a [HW] or [HW1] array
        class_num: num of classes
    Returns:
        one_hot: a 3D array of one_hot label (dtype=np.uint8), C=num of classes
    '''
    one_hot = np.zeros([label.shape[0], label.shape[1], class_num], dtype=np.uint8)
    for i in range(class_num):
        one_hot[:, :, i] = (label == i)  # TODO: need test [HW1]
    return one_hot


def one_hot_2(label, label_values):
    """
    One hot code the RBG label by replacing each pixel value with a vector of length num_classes
    Note: If class_dict is RGB, the label must be RGB(not BGR).
    Args:
        label: a [HWC] array, and C=3(be carefull about RGB or BGR)
        label_values: A list per class's color values.  [[0,0,0], [255,255,255], ]
    Returns:
        one_hot: one_hot label, C=num of classes
    """
    semantic_map = []
    for colour in label_values:
        equality = np.equal(label, colour)
        class_map = np.all(equality, axis=-1)
        semantic_map.append(class_map)
    semantic_map = np.stack(semantic_map, axis=-1).astype(np.uint8)

    return semantic_map


def one_hot_3(label, class_num):
    '''One hot code the label, classification result.
    Args:
        label: a [1] or [N1] array
        class_num: num of classes
    Returns:
        one_hot: a [NC] array of one_hot label, C=num of classes
    '''
    one_hot = np.zeros([label.shape[0], class_num], dtype=label.dtype)
    for i in range(class_num):
        one_hot[:, i] = (label == i)
    return one_hot


def class_label(label, label_values):
    '''
    Convert RGB label to 2D [HW] array, each pixel value is the classified class key.
    '''
    semantic_map = np.zeros(label.shape[:2], label.dtype)
    for i in range(len(label_values)):
        equality = np.equal(label, label_values[i])
        class_map = np.all(equality, axis=-1)
        semantic_map[class_map] = i
    return semantic_map


def reverse_one_hot(one_hot):
    '''Transform a 3D array in one-hot format (depth is num_classes),
    to a 2D array, each pixel value is the classified class key.
    '''
    return np.argmax(one_hot, axis=2)  # set axis=2 to limit the input is 3D


def colour_code_label(label, label_values, add_image=None, save_path=None):
    '''
    Given a [HW] array of class keys(or one hot[HWC]), colour code the label;
    also can weight the colour coded label and image, maybe save the final result.

    Args:
        label: single channel array where each value represents the class key.
        label_values: A list per class's color values. [[0,0,0], [255,255,255], ]
    Returns:
        Colour coded label or just save image return none.
    '''
    label, colour_codes = np.array(label), np.array(label_values)
    if len(label) == 3:
        label = np.argmax(label, axis=2)  # [HWC] -> [HW]
    color_label = colour_codes[label.astype(int)]  # TODO:此处直接uint8有错误
    color_label = color_label.astype(np.uint8)

    if add_image is not None:
        if add_image.shape != color_label.shape:
            cv2.resize(color_label, (add_image.shape[1], add_image.shape[0]),
                       interpolation=cv2.INTER_NEAREST)
        add_image = cv2.addWeighted(add_image, 0.7, color_label, 0.3, 0)
        if save_path is None:
            return color_label, add_image

    if save_path is not None:
        cv2.imwrite(save_path, color_label, [1, 100])
        if add_image is not None:
            cv2.imwrite(rename_file(save_path, addstr='mask'), add_image, [1, 100])
        return  # no need to return label if saved

    return color_label


def mask_img(image, label, mask_value=[0, 0, 0]):
    '''Mask image may with multi-bands with a specified value of label.
    Note: mask_value is value list.
    '''
    equality = np.equal(label, mask_value)
    mask = np.all(equality, axis=-1)
    image[mask] = [0, 0, 0]
    return image


# **********************************************
# ******** Common data Pre-treatment ***********
# **********************************************
def slide_crop(image, crop_params=[256, 256, 128], pad_mode=0, ifbatch=False):
    '''
    Slide crop image([HW] or [HWC] ndarray) into small piece,
    return list of sub_image or a [NHWC] array.

    Args:
        crop_params: [H, W, stride] (default=[256, 256, 128])

        pad_mode: One of the [-1, 0, 1] int values,
            -1 - Drop out the rest part;
            0 - Pad image at the end of W & H for fully cropping;
            1 - Pad image before and after W & H for fully cropping.
        ifbatch: Ture-return [NHWC] array; False-list of image.
    Return:
        size: [y, x]
            y - Num of images in the row direction.
            x - Num of images in the col direction.

    Carefully: If procided clipping parameters cannot completely crop the entire image,
        then it cannot be restored to original size during the recovery process.
    '''
    crop_h, crop_w, stride = crop_params
    H, W = image.shape[:2]

    if pad_mode < 0:
        # Adjust crop_params according to image_size
        crop_h = H if crop_h > H else crop_h
        crop_w = W if crop_w > W else crop_w

    h_res, w_res = (H-crop_h) % stride, (W-crop_w) % stride
    if h_res or w_res:  # Cannot completely slide-crop the target image
        sh = crop_h if H < crop_h else stride
        sw = crop_w if W < crop_w else stride
        # Adjust image_size according to crop_params
        if pad_mode >= 0:
            image, _ = pad_array(image, crop_h, crop_w, sh, sw, pad_mode)
        elif pad_mode == -1:
            if h_res:
                image = image[:-h_res, :]
            if w_res:
                image = image[:, :-w_res]
        H, W = image.shape[:2]  # Update image size

    image_list = []
    y = 0  # y:H(row)
    for i in range((H-crop_h)//stride + 1):
        x = 0  # x:W(col)
        for j in range((W-crop_w)//stride + 1):
            image_list.append(image[y:y+crop_h, x:x+crop_w].copy())
            x += stride
        y += stride
    size = [i+1, j+1]

    if ifbatch:
        batch_size = len(image_list)
        if batch_size == 1:
            return np.expand_dims(image_list[0], axis=0), size
        else:
            image_bantch = np.stack(image_list, axis=0)
            return image_bantch, size

    return image_list, size


def reverse_slide_crop(patches, crop_params, crop_info, HWC=True):
    '''
    Combine small patches by slide_crop into a big one.
    Args:
        patches: list of patches
        crop_params: [sub_h, sub_w, crop_stride]
        crop_info: [rows, cols]
            rows - Num of images in the row direction.
            cols - Num of images in the col direction.
    Returns:
        out_array: [HWC] or [CHW] ndarray.
    '''
    rows, cols = crop_info
    h, w, stride = crop_params
    # label = np.array(label)  # Tensor -> Array
    out_h, out_w = (rows-1)*stride+h, (cols-1)*stride+w
    if HWC:
        out_array = np.zeros([out_h, out_w, patches[0].shape[-1]], dtype=patches[0].dtype)  # [HWC]
    else:
        out_array = np.zeros([patches[0].shape[-1], out_h, out_w], dtype=patches[0].dtype)  # [HWC]
    y = 0  # y=h=row
    for i in range(rows):
        x = 0  # x=w=col
        for j in range(cols):
            if HWC:
                out_array[y:y+h, x:x+w] = patches[i*cols+j]
            else:
                out_array[:, y:y+h, x:x+w] = patches[i*cols+j]
            x += stride
        y += stride
    return out_array


def pad_array(array, kh, kw, sh, sw, mode=0):
    '''Pad array according kernel size and crop stride.

    Args:
        kh, kw: kernel height, kernel width.
        sh, sw: height directional stride, width directional stride.
        mode:
            0 - pad at the end of H/W dimension
            1 - pad at the begain and end of H/W dimension
    '''
    h, w = array.shape[:2]
    d = len(array.shape)
    pad_h, pad_w = sh - (h-kh) % sh, sw - (w-kw) % sw
    if mode == 0:
        pad_h, pad_w = (0, pad_h), (0, pad_w)
    elif mode == 1:
        pad_h = (pad_h//2, pad_h//2+1) if pad_h % 2 else (pad_h//2, pad_h//2)
        pad_w = (pad_w//2, pad_w//2+1) if pad_w % 2 else (pad_w//2, pad_w//2)
    pad_params = (pad_h, pad_w) if d == 2 else (pad_h, pad_w, (0, 0))
    return np.pad(array, pad_params, mode='constant'), pad_params


def scale_img(image, new_size=[256]):
    '''
    Scale the image (keep aspect ratio,
    let the shortest side equal to the target heigth/width,
    then crop it into the targe height and width).
    Args:
        new_size - a tuple may have only one element(H=W) or two elements(H, W).
    '''
    if len(new_size) == 2:
        H, W = new_size
        image = cv2.resize(image, (W, H))  # TODO: not support multi-bands
    elif len(new_size) == 1:
        h, w = image.shape[:2]
        if w > h:  # if image width > image height
            H, W = new_size[0], int(w*new_size[0]/h)
            st = int((W-H)/2)
            image = cv2.resize(image, (W, H))[:, st:st+H]
        else:  # if image height > image width
            H, W = int(w*new_size[0]/h), new_size[0]
            st = int((H-W)/2)
            image = cv2.resize(image, (W, H))[st:st+H, :]
    else:
        ValueError('Incorrect new_size!')

    return image


def resize_img(image, new_size=(256, 256), interpolation=cv2.INTER_LINEAR):
    """ Resize the image into new shape `new_size`, support multi-bands data.
    """
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
        band_num = 1
    elif len(image.shape) == 3:
        band_num = image.shape[2]

    if band_num == 1 or band_num == 3:
        image = cv2.resize(image, new_size[::-1], interpolation=interpolation)
    else:
        new_image = np.zeros((new_size[0], new_size[1], band_num), dtype=image.dtype)
        for c in range(0, band_num):
            new_image[:, :, c] = cv2.resize(image[:, :, c], new_size[::-1],
                                            interpolation=interpolation)
        image = new_image

    return image


def unify_imgsize(img_dir, size=(256, 256), interpolation=cv2.INTER_NEAREST):
    '''
    Unify image size.
    Args:
        size: Uniform size(must be tuple)
        interpolation: Interpolation method of zoom image
    '''
    num = 1
    image_names = sorted(os.listdir(img_dir))
    for name in tqdm(image_names):
        img = cv2.imread(img_dir+'/'+name, -1)
        if img.shape[:2] != size:
            img = cv2.resize(img, size[::-1], interpolation)
        cv2.imwrite(img_dir+'/'+name, img, [1, 100])
        num += 1


def label_pretreat(label_dir, label_values):
    '''
    Pre-treat the orignal RGB label, to fix the apparent bug.
    (Actually it eliminate the wrong colors that are not in class_dict)
    By the way, unify the dtype of label imgs to png.
    '''
    l_names = filelist(label_dir, ifPath=True)
    for name in tqdm(l_names):
        label = cv2.imread(name, 1)  # read in RGB
        os.remove(name)
        name = os.path.splitext(name)[0] + '.png'
        new_label = np.zeros(label.shape, label.dtype)
        # Fix the color(stand for a class) by class-info
        for color in label_values:
            equality = np.equal(label, color)
            ind_mat = np.all(equality, axis=-1)
            new_label[ind_mat] = color  # this color list can be customized
        cv2.imwrite(name, new_label)  # new_label-BGR(according to class_dict)


# **********************************************
# ********** Commen data augment ***************
# **********************************************
def filp_array(array, flipCode):
    '''Filp an [HW] or [HWC] array vertically or horizontal according to flipCode.'''
    if flipCode != -1:
        array = np.flip(array, flipCode)
    elif flipCode == -1:
        array = np.flipud(array)
        array = np.fliplr(array)
    return array


def resized_crop(image, i, j, h, w, size, interpolation=cv2.INTER_LINEAR):
    '''Crop the given ndarray image and resize it to desired size.
    Args:
        i: Upper pixel coordinate.
        j: Left pixel coordinate.
        h: Height of the cropped image.
        w: Width of the cropped image.
        size: (Height, Width) must be tuple
    '''
    h_org, w_org = image.shape[:2]
    i, j = max(0, i), max(0, j)
    h, w = min(h_org-i, h), min(w_org-j, w)
    image = image[i:i+h, j:j+w]

    image = resize_img(image, new_size=size, interpolation=interpolation)
    return image


def center_crop(array, crop_hw=(256, 256)):
    ''' Crops the given image(label) at the center.
    '''
    h, w = array.shape[:2]
    th, tw = crop_hw
    th, tw = min(h, th), min(w, tw)

    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))

    array = array[i:i+th, j:j+tw]
    return array


def random_crop(array, crop_hw=(256, 256)):
    '''
    Crop image(label) randomly
    '''
    crop_h, crop_w = crop_hw
    if (crop_h < array.shape[0] and crop_w < array.shape[1]):
        x = np.random.randint(0, array.shape[0] - crop_h)  # row
        y = np.random.randint(0, array.shape[1] - crop_w)  # column
        return array[x:x + crop_h, y:y + crop_w]

    elif (crop_h == array.shape[0] and crop_w == array.shape[1]):
        return array

    else:
        raise Exception('Crop size > image.shape')


def random_crop_pair(image, label, crop_hw=(256, 256)):
    '''
    Crop image and label randomly

    '''
    crop_h, crop_w = crop_hw
    if image.shape[:2] != label.shape[:2]:
        raise Exception('Image and label must have the same shape')
    if (crop_h < image.shape[0] and crop_w < image.shape[1]):
        x = np.random.randint(0, image.shape[0] - crop_h)  # row
        y = np.random.randint(0, image.shape[1] - crop_w)  # column
        # label maybe multi-channel[H,W,C] or one-channel [H,W]
        return image[x:x + crop_h, y:y + crop_w], label[
            x:x + crop_h, y:y + crop_w]
    elif (crop_h == image.shape[0] and crop_w == image.shape[1]):
        return image, label
    else:
        raise Exception('Crop size > image.shape')


def random_crop_balance(image, label, crop_hw=(256, 256), num_classes=0):
    '''
    Crop image(label) randomly for serval times(now four times most),
    and return the one in which per class RATIO most balancing.
    Don't support RGB label now.
    Args:
        label: 1. [HW]; 2. [HW1]; 3. one_hot-[HWC]; 4. rgb-[HWC]-目前不支持rbg!!!
            Note: 1&2 class_num need to be specified!!!
        num_classes: default=0, only one_hot label don't have to specify.
    Returns:
        image: croped image
        label: croped laebl
    '''
    crop_h, crop_w = crop_hw
    if (image.shape[0] != label.shape[0]) or (image.shape[1] != label.shape[1]):
        raise Exception('Image and label must have the same dimensions!')

    if (crop_w < image.shape[1]) and (crop_h < image.shape[0]):
        x, y = [0, 0, 0, 0], [0, 0, 0, 0]
        rate = [1., 1., 1., 1.]  # store min RATIO
        sum_area = crop_h * crop_w

        if len(label.shape) == 2 or label.shape[-1] == 1:  # [HW] or [HW1]
            for i in range(4):  # try four times and choose the max rate's x,y
                x[i] = np.random.randint(0, image.shape[1] - crop_w)  # W
                y[i] = np.random.randint(0, image.shape[0] - crop_h)  # H
                tmp_label = label[y[i]:y[i] + crop_h, x[i]:x[i] + crop_w].crop()

                for j in range(num_classes):
                    indArr = [tmp_label == j]
                    tmp_rate = np.sum(indArr) / sum_area
                    if tmp_rate == 0:
                        rate[i] = tmp_rate
                        break
                    elif tmp_rate < rate[i]:
                        rate[i] = tmp_rate

        else:  # [HWC] - only support one_hot label now
            for i in range(4):
                x[i] = np.random.randint(0, image.shape[1] - crop_w)  # W
                y[i] = np.random.randint(0, image.shape[0] - crop_h)  # H
                tmp_label = label[y[i]:y[i] + crop_h, x[i]:x[i] + crop_w, :].crop()

                # For one_hot label
                for j in range(tmp_label.shape[2]):  # traverse all channel-class
                    indArr = tmp_label[:, :, j]
                    tmp_rate = np.sum(indArr) / sum_area
                    if tmp_rate == 0:
                        rate[i] = tmp_rate
                        break
                    elif tmp_rate < rate[i]:
                        rate[i] = tmp_rate

        ind = rate.index(max(rate))  # choose the max RATIO area
        x, y = x[ind], y[ind]

        label = label[y:y + crop_h, x:x + crop_w]
        image = image[y:y + crop_h, x:x + crop_w]
        return image, label

    elif (crop_w == image.shape[1] and crop_h == image.shape[0]):
        return image, label

    else:
        raise Exception('Crop shape exceeds image dimensions!')


def randomShiftScaleRotate(image,
                           mask=None,
                           shift_limit=(-0.0, 0.0),
                           scale_limit=(-0.0, 0.0),
                           rotate_limit=(-0.0, 0.0),
                           aspect_limit=(-0.0, 0.0),
                           borderMode=cv2.BORDER_CONSTANT,
                           p=0.5):
    """
    Random shift scale rotate image (support multi-band) may be with mask.

    Args:
        p (float): Probability of rotation.
    """
    if np.random.random() < p:
        if len(image.shape) > 2:
            height, width, channel = image.shape
        else:
            (height, width), channel = image.shape, 1

        angle = np.random.uniform(rotate_limit[0], rotate_limit[1])
        scale = np.random.uniform(1 + scale_limit[0], 1 + scale_limit[1])
        aspect = np.random.uniform(1 + aspect_limit[0], 1 + aspect_limit[1])
        sx = scale * aspect / (aspect**0.5)
        sy = scale / (aspect**0.5)
        dx = round(np.random.uniform(shift_limit[0], shift_limit[1]) * width)
        dy = round(np.random.uniform(shift_limit[0], shift_limit[1]) * height)

        cc = np.math.cos(angle / 180 * np.math.pi) * sx
        ss = np.math.sin(angle / 180 * np.math.pi) * sy
        rotate_matrix = np.array([[cc, -ss], [ss, cc]])

        box0 = np.array([
            [0, 0],
            [width, 0],
            [width, height],
            [0, height],
        ])
        box1 = box0 - np.array([width / 2, height / 2])
        box1 = np.dot(box1, rotate_matrix.T) + np.array(
            [width / 2 + dx, height / 2 + dy])

        box0 = box0.astype(np.float32)
        box1 = box1.astype(np.float32)
        mat = cv2.getPerspectiveTransform(box0, box1)

        if channel > 3:
            for c in range(channel):
                band = image[:, :, c]
                image[:, :, c] = cv2.warpPerspective(
                    band, mat, (width, height),
                    flags=cv2.INTER_LINEAR, borderMode=borderMode)
        else:
            image = cv2.warpPerspective(
                image, mat, (width, height),
                flags=cv2.INTER_LINEAR, borderMode=borderMode)
        if mask is not None:
            mask = cv2.warpPerspective(
                mask, mat, (width, height),
                flags=cv2.INTER_LINEAR, borderMode=borderMode)
    if mask is not None:
        return image, mask
    else:
        return image


def rotate_pair_img(xb, yb, angle):
    '''rotate xb, yb'''
    h, w = xb.shape[0], xb.shape[1]
    M_rotate = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
    xb = cv2.warpAffine(xb, M_rotate, (w, h))
    yb = cv2.warpAffine(yb, M_rotate, (w, h))
    return xb, yb


def randomHueSaturationValue(image,
                             hue_shift_limit=(-180, 180),
                             sat_shift_limit=(-255, 255),
                             val_shift_limit=(-255, 255),
                             u=0.5):
    if np.random.random() < u:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(image)
        hue_shift = np.random.randint(hue_shift_limit[0],
                                      hue_shift_limit[1] + 1)
        hue_shift = np.uint8(hue_shift)
        h += hue_shift
        sat_shift = np.random.uniform(sat_shift_limit[0], sat_shift_limit[1])
        s = cv2.add(s, sat_shift)
        val_shift = np.random.uniform(val_shift_limit[0], val_shift_limit[1])
        v = cv2.add(v, val_shift)
        image = cv2.merge((h, s, v))
        #image = cv2.merge((s, v))
        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

    return image


def randomColorAugment(image, brightness=0.1, contrast=0.1):
    ''' Randomly jotter the brightness and contrast of each band in ndarray imagery.
    '''
    if brightness > 0:
        brightness_factor = np.random.uniform(max(0, 1-brightness), 1+brightness)
        if brightness_factor > 1:
            alpha = brightness_factor - 1
            degenerate = np.ones_like(image) * 255
        elif brightness_factor <= 1:
            alpha = 1 - brightness_factor
            degenerate = np.zeros_like(image)
        image = cv2.addWeighted(degenerate, alpha, image, (1-alpha), 0)

    # Adjust contrast, saturation and hue reference: https://zhuanlan.zhihu.com/p/24425116
    if contrast > 0:
        contrast_factor = np.random.uniform(max(0, 1-contrast), 1+contrast)
        image = np.clip(image * contrast_factor, 0, 255).astype(np.uint8)
    return image


def random_noise(image, mode='gaussian', seed=None, clip=True, **kwargs):
    """
    Function to add random noise of various types to a image.

    Parameters
    ----------
    image : ndarray
        Input image data sized of [HW] or [HWC] (support multi-band), from range of (0~255).
    mode : str, optional
        One of the following strings, selecting the type of noise to add:

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
    seed : int, optional
        If provided, this will set the random seed before generating noise,
        for valid pseudo-random comparisons.
    clip : bool, optional
        If True (default), the output will be clipped after noise applied
        for modes `'speckle'`, `'poisson'`, and `'gaussian'`. This is
        needed to maintain the proper image data range. If False, clipping
        is not applied, and the output may extend beyond the range [0, 255].
    mean : float, optional
        Mean of random distribution. Used in 'gaussian' and 'speckle'.
        Default : 0.
    var : float, optional
        Variance of random distribution. Used in 'gaussian' and 'speckle'.
        Note: variance = (standard deviation) ** 2. Default : 0.01
    local_vars : ndarray, optional
        Array of positive floats, same shape as `image`, defining the local
        variance at every image point. Used in 'localvar'.
    amount : float, optional
        Proportion of image pixels to replace with noise on range [0, 1].
        Used in 'salt', 'pepper', and 'salt & pepper'. Default : 0.01
    salt_vs_pepper : float, optional
        Proportion of salt vs. pepper noise for 's&p' on range [0, 1].
        Higher values represent more salt. Default : 0.5 (equal amounts)

    Returns
    -------
    out : ndarray
        Output floating-point image data on range [0, 255].

    Notes
    -----
    Speckle, Poisson, Localvar, and Gaussian noise may generate noise outside
    the valid image range. The default is to clip (not alias) these values,
    but they may be preserved by setting `clip=False`. Note that in this case
    the output may contain values outside the ranges [0, 255].
    Use this option with care.

    Because of the prevalence of exclusively positive floating-point images in
    intermediate calculations, it is not possible to intuit if an input is
    signed based on dtype alone. Instead, negative values are explicitly
    searched for. Only if found does this function assume signed input.
    Unexpected results only occur in rare, poorly exposes cases (e.g. if all
    values are above 50 percent gray in a signed `image`). In this event,
    manually scaling the input to the positive domain will solve the problem.

    The Poisson distribution is only defined for positive integers. To apply
    this noise type, the number of unique values in the image is found and
    the next round power of two is used to scale up the floating-point result,
    after which it is scaled back down to the floating-point image range.

    To generate Poisson noise against a signed image, the signed image is
    temporarily converted to an unsigned image in the floating point domain,
    Poisson noise is generated, then it is returned to the original range.

    """
    mode = mode.lower()

    if seed is not None:
        np.random.seed(seed=seed)

    allowedtypes = {
        'gaussian': 'gaussian_values',
        'localvar': 'localvar_values',
        'poisson': 'poisson_values',
        'salt': 'sp_values',
        'pepper': 'sp_values',
        's&p': 's&p_values',
        'speckle': 'gaussian_values'}

    kwdefaults = {
        'mean': 0.,
        'var': 0.01,
        'amount': 0.01,
        'salt_vs_pepper': 0.5,
        'local_vars': np.zeros_like(image) + 0.01}

    allowedkwargs = {
        'gaussian_values': ['mean', 'var'],
        'localvar_values': ['local_vars'],
        'sp_values': ['amount'],
        's&p_values': ['amount', 'salt_vs_pepper'],
        'poisson_values': []}

    for key in kwargs:
        if key not in allowedkwargs[allowedtypes[mode]]:
            raise ValueError('%s keyword not in allowed keywords %s' %
                             (key, allowedkwargs[allowedtypes[mode]]))

    # Set kwarg defaults
    for kw in allowedkwargs[allowedtypes[mode]]:
        kwargs.setdefault(kw, kwdefaults[kw])

    img_type = image.dtype
    if mode == 'gaussian':
        noise = np.random.normal(kwargs['mean'], kwargs['var'] ** 0.5,
                                 image.shape)
        out = image + (noise*128).astype(img_type)

    elif mode == 'localvar':
        # Ensure local variance input is correct
        if (kwargs['local_vars'] <= 0).any():
            raise ValueError('All values of `local_vars` must be > 0.')

        # Safe shortcut usage broadcasts kwargs['local_vars'] as a ufunc
        noise = np.random.normal(0, kwargs['local_vars'] ** 0.5)
        out = image + (noise * 128).astype(img_type)

    elif mode == 'poisson':
        # Determine unique values in image & calculate the next power of two
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))

        # Generating noise for each unique value in image.
        out = (np.random.poisson(image * vals) / float(vals)).astype(img_type)

    elif mode == 'salt':
        # Re-call function with mode='s&p' and p=1 (all salt noise)
        out = random_noise(image, mode='s&p', seed=seed,
                           amount=kwargs['amount'], salt_vs_pepper=1.)

    elif mode == 'pepper':
        # Re-call function with mode='s&p' and p=1 (all pepper noise)
        out = random_noise(image, mode='s&p', seed=seed,
                           amount=kwargs['amount'], salt_vs_pepper=0.)

    elif mode == 's&p':
        out = image.copy()
        p = kwargs['amount']
        q = kwargs['salt_vs_pepper']
        flipped = np.random.choice([True, False], size=image.shape,
                                   p=[p, 1 - p])
        salted = np.random.choice([True, False], size=image.shape,
                                  p=[q, 1 - q])
        peppered = ~salted
        out[flipped & salted] = 255
        out[flipped & peppered] = 0

    elif mode == 'speckle':
        noise = np.random.normal(kwargs['mean'], kwargs['var'] ** 0.5,
                                 image.shape)
        out = image + (image * noise).astype(img_type)

    # Clip back to original range, if necessary
    if clip:
        out = np.clip(out, 0, 255)

    return out


def blur(image, ksize=3):
    if len(image.shape) > 2:
        for c in range(image.shape[2]):
            band = image[:, :, c]
            image[:, :, c] = cv2.blur(band, (ksize, ksize))
    else:
        image = cv2.blur(image, (ksize, ksize))
    return image


def gamma_transform(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


def random_gamma_transform(img, gamma_vari):
    log_gamma_vari = np.log(gamma_vari)
    alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)
    gamma = np.exp(alpha)
    return gamma_transform(img, gamma)


# **********************************************
# ************ Main functions ******************
# **********************************************
def crop_imgs(image_dir, out_dir=None, crop_params=None, ifPad=True):
    ''' Slide crop images into small piece and save them. '''
    if out_dir is None:
        out_dir = image_dir

    image_names = sorted(os.listdir(image_dir))
    for name in tqdm(image_names):
        image = cv2.imread(image_dir+'/'+name, -1)
        # 附加操作
        # h, w = image.shape[:2]
        # image = cv2.resize(image, (int(w*0.7), int(h*0.7)))
        imgs, _ = slide_crop(image, crop_params, ifPad)
        num = len(imgs)
        for i in range(num):
            save_name = rename_file(name, addstr="_%d" % (i+1))  # TODO: 子图编号的位数
            cv2.imwrite(out_dir+'/'+save_name, imgs[i], [1, 100])


if __name__ == '__main__':
    # main()
    # main_of_imgAndlabel_ops()
    # in_dir = '/home/tao/Code/Result/CVPR/测试集_真实/val_labels_visual'
    # in_dir = 'D:/Data_Lib/Other/Small/6/train_labels'
    # out_dir = '/home/tao/Code/Result/CVPR/测试集_真实/val_labels'
    # in_dir = '/home/tao/Data/RBDD/BackUp/Orignal_data/val_labels'
    # out_dir = '/home/tao/Data/RBDD/512/val_labels'
    # main_of_img_ops(in_dir, out_dir)
    # crop_imgs(in_dir, out_dir, [512, 512, 512])

    pass


"""
BackUp

def data_augment(image, label=None, crop_size=None, zoom_size=None, if_flip=True, if_roate=True):
    '''
    Simple data augment function to random crop,flip and roate image and label.
    Args:
        image: array of image, [HWC] or [HW1] or [HW].
        label: array of label, [HWC] or [HW1] or [HW].
        crop_size: [h, w]
        zoom_size: [h, w]
        if_flip: if flip the image(and label), defualt = True
        if_roate: if roate the image(and label), defualt = True

    Returns:
        image, label: processed image and label
    '''
    if label is None:
        if crop_size is not None:
            image = random_crop(image, crop_size[0], crop_size[1])
        if zoom_size is not None:
            image = cv2.resize(
                image, (zoom_size[1], zoom_size[0]), interpolation=cv2.INTER_LINEAR)
        # Flip
        if if_flip and np.random.randint(0, 2):
            image = cv2.flip(image, 1)
        if if_flip and np.random.randint(0, 2):
            image = cv2.flip(image, 0)
        # Roate
        iflag = np.random.randint(0, 2)
        if if_roate and iflag:
            angle_table = [90, 180, 270]
            angle = angle_table[np.random.randint(0, 3)]
            h, w = image.shape[0], image.shape[1]
            M_rotate = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
            image = cv2.warpAffine(image, M_rotate, (w, h))
        return image
    else:
        if crop_size is not None:
            image, label = random_crop_2(image, label, crop_size[0], crop_size[1])
        if zoom_size is not None:
            image = cv2.resize(image, (zoom_size[1], zoom_size[0]), cv2.INTER_LINEAR)
            label = cv2.resize(label, (zoom_size[1], zoom_size[0]), cv2.INTER_NEAREST)
        # Flip
        if if_flip and np.random.randint(0, 2):
            image, label = cv2.flip(image, 1), cv2.flip(label, 1)
        if if_flip and np.random.randint(0, 2):
            image, label = cv2.flip(image, 0), cv2.flip(label, 0)
        # Roate
        iflag = np.random.randint(0, 2)
        if if_roate and iflag:
            angle_table = [90, 180, 270]
            angle = angle_table[np.random.randint(0, 3)]
            image, label = rotate(image, label, angle)
        return image, label

def main_of_hdf5(img_dir, label_dir, class_dict_path, h5_path):
    ''' Cover images and labels to hdf5 format. '''
    _, class_values = get_label_info(class_dict_path)
    img2hdf5(img_dir, h5_path)
    label2hdf5(label_dir, h5_path, label_values=class_values)


# **********************************************
# ************** HDF5 tools ********************
# **********************************************
def label2hdf5(input_dir, output_path, label_values=None, class_num=None):
    '''
    Transform a label image into one-hot format (depth is num_classes),
    and save them all in a dataset(key:"labels") of a h5 flie.

    Args:
        input_dir: The dir of label images [HW] or [HWC](BGR)
        output_path: The whole path of the output h5 flie.
        label_values: A dictionairy of class--> pixel values, defualt=None
        class_num: Num of classes, defualt=None
            Note:
                1. If class_num is specified, input labels is [HW](imread in gray mode),
                    call one_hot_1
                2. If label_values is specified, input labels is [HWC]BGR, call one_hot_2;

    Returns
        None, but will create a 4d dataset store all one hot labels(in a h5 file).

    Notice:
        the dtype of the dataset is uint8(np.uint8).
        the key of labels dataset is "label".

    '''
    print("*******Execute label2hdf5()*******")
    input_names = sorted(os.listdir(input_dir))  # only the name of labels
    # Carefull!! Since the os.listdir() return a list in atribute order, sort it

    # Read first of them to get shape
    tmp_input = cv2.imread(input_dir + "/" + input_names[0], -1)
    size = [0, 0, 0, 0]  # NHWC
    size[0] = len(input_names)  # get N
    size[1], size[2] = tmp_input.shape[0], tmp_input.shape[1]  # get H,W

    if class_num is not None:  # [HW], class_num must not None
        size[3] = class_num
    elif label_values is not None:  # [HWC]-BGR
        size[3] = size[3] = len(label_values)
    else:
        ValueError("label_values or class_num must specify one.")

    # Open(or create) a hdf5 flie to save all the labels
    f = h5py.File(output_path, 'a')
    dataset = f.create_dataset("label", shape=size, dtype=np.uint8)  # create a 4d dataset
    # Treat per label in the list
    if class_num is not None:  # [HW], class_num must not None
        for i in tqdm(range(len(input_names))):
            label = cv2.imread(input_dir + "/" + input_names[i], 0)
            dataset[i, :] = one_hot_1(label, class_num)  # return uint8 array
    elif label_values is not None:  # [HWC]-RGB
        target = open(os.path.dirname(output_path) + "/train_gt.txt", 'w')
        for i in tqdm(range(len(input_names))):
            label = cv2.imread(input_dir + "/" + input_names[i], -1)
            dataset[i, :] = one_hot_2(label, label_values)  # return uint8 array
            target.write(input_names[i]+'\n')
    print(dataset.shape, dataset.dtype)
    print("*******Finish label2hdf5()*******")
    f.close()


def img2hdf5(input_dir, output_path):
    '''
    Save images and their names into h5 file

    Args:
        input_dir: The dir of images.
        output_path: The whole path of the output h5 flie.

    Returns:
        None.
        But will create a h5 file with a 4d dataset store all images(RGB),
            and a 1d dataset store all their names.
    Notice:
        the dtype of the dataset is uint8(np.uint8).
        the key of image dataset is "image".(RGB)
        the key of image name dataset is "name"

    '''
    print("*******Execute img2hdf5()*******")
    input_names = sorted(os.listdir(input_dir))  # only the name of images
    # Carefull!! Since the os.listdir() return a list in atribute order, sort it
    names = []  # 将文件名转utf8编码，才能存入hdf5的dataset中
    for j in input_names:
        names.append(j.encode('utf8'))

    # Read first of them to get shape
    tmp_input = load_image(input_dir + "/" + input_names[0], 1)
    size = [0, 0, 0, 0]  # NHWC
    size[0] = len(input_names)  # get N
    size[1:] = tmp_input.shape  # get HWC

    # Open(or create) a hdf5 flie to save all the images and their names
    f = h5py.File(output_path, 'w')
    f.create_dataset("name", data=names)  # 创建name数据集存储images 的utf8编码的文件名
    # Create an empty 4d dataset(image) to store images
    dataset = f.create_dataset("image", shape=size, dtype=np.uint8)
    # Treat per img in the list
    target = open(os.path.dirname(output_path) + "/train.txt", 'w')
    for i in tqdm(range(len(input_names))):
        input_path = input_dir + "/" + input_names[i]  # the whole path
        img = load_image(input_path, 1)
        # Extension pocessing
        # for c in range(img.shape[-1]):
        #     img[:, :, c] = cv2.equalizeHist(img[:, :, c])
        dataset[i, :] = img
        target.write(input_names[i]+'\n')

    print(dataset.shape, dataset.dtype)
    print("*******Finish img2hdf5()*******")
    f.close()


def img2hdf5_2(input_dir, output_path, newsize=None):
    '''
    For classified, save images and their names into h5 file,
    meanwhile make their labels[NC].

    Args:
        input_dir: The dir of images(in several folders).
        output_path: The whole path of the output h5 flie.

    Returns:
        None.
        But will create a h5 file with a 4d dataset store all images(RGB),
            and a 1d dataset store all their names.
    Notice:
        the dtype of the dataset is uint8(np.uint8).(RGB)
        the key of image dataset is "image".
        the key of label dataset is "label".
        the key of image name dataset is "name"
        the key of class name dataset is "class"

    '''
    print("*******Execute img2hdf5()*******")
    # Fisrt travals get total image num and all class names and image names
    image_names = []  # all image names
    folder_names = sorted(os.listdir(input_dir))  # also name of classes
    for i, f in enumerate(folder_names):
        file_names = sorted(os.listdir(input_dir+'/'+f))  # name of images
        image_names += file_names

    utf_names = [name.encode('utf8') for name in image_names]  # 转utf8存入
    utf_classNames = [name.encode('utf8') for name in folder_names]

    # Read first of them to get shape
    tmp_input = load_image(os.path.join(input_dir, folder_names[0], image_names[0]), 1)
    img_size = [0, 0, 0, 0]  # NHWC(channel), size of image dataset
    label_size = [0, 0]  # NC(classnum), size of label dataset
    img_size[0] = label_size[0] = len(image_names)  # get N
    img_size[1:] = tmp_input.shape  # get HWC si.extend(ze
    label_size[1] = len(folder_names)  # get class num

    # Open(or create) a hdf5 flie to save all the images and their names
    f = h5py.File(output_path, 'w')
    f.create_dataset("name", data=utf_names)  # 创建name数据集存class_dict储images 的utf8编码的文件名
    f.create_dataset('class', data=utf_classNames)
    # Create an empty 4d dataset(image) to store images
    imageSet = f.create_dataset("image", shape=img_size, dtype=np.uint8)
    labelSet = f.create_dataset("label", shape=label_size, dtype=np.uint8)
    # Save per img.extend(
    i = 0
    for c, fo in tqdm(enumerate(folder_names)):
        file_names = sorted(os.listdir(input_dir+'/'+fo))
        for fi in file_names:
            img = load_image(os.path.join(input_dir, fo, fi), 1)
            if newsize is not None:
                img = cv2.resize(img, (newsize[1], newsize[0]))
            imageSet[i, :] = img
            labelSet[i, c] = 1
            i += 1

    # print(imageSet.shape, imageSet.dtype)
    print("*******Finish img2hdf5()*******")
    f.close()


def sp_noise(image, gamma=0.01):
    ''' Add Salt-Pepper noise to an image [0,255].

    Args:
        gamma (float): It's evaluated at [0, 0.5);
            Pixels in image [0, gamma) is set to 0, (1-gamma, 1) is set to 255.
    '''
    prob_mat = np.random.random(size=image.shape[:2])
    noise_image = image.copy()
    noise_image[prob_mat < gamma, None] = 0
    noise_image[prob_mat > 1 - gamma, None] = 255
    return noise_image


def randpixel_noise(image, p=0.01):
    '''Randomly perturbed the values of some pixels in the image [0,255].

    Args:
        p: The probability that each pixel is perturbed.
    '''
    prob_mat = np.random.random(size=image.shape[:2])
    noise = np.random.randint(0, 256, size=image.shape, dtype=image.dtype)
    noise[prob_mat >= p] = 0

    noise_image = image.copy()
    noise_image[prob_mat < p, None] = 0
    noise_image += noise

    return noise_image

"""
