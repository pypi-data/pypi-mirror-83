# -*- coding:utf-8 -*-
'''
Utils for Pytorch.

Version 1.0  2020-10-29 16:30:04 by QiJi
    Common tools in PyTorch environment were collected.
TODO:
1. xxx

'''
import os
import torch
import torch.nn.functional as F
import numpy as np
import shutil
from .dldata import vote_combine


# **************************************************
# *************** Tensor operations ****************
# **************************************************
def random_crop_tensor(tensor, crop_hw, dataformat='NCHW'):
    crop_h, crop_w = crop_hw
    if dataformat == 'NCHW':
        assert crop_h <= tensor.shape[2]
        assert crop_w <= tensor.shape[3]
        x = np.random.randint(0, tensor.shape[2] - crop_h)  # row
        y = np.random.randint(0, tensor.shape[3] - crop_w)  # column
        tensor = tensor[:, :, x:x+crop_h, y:y+crop_w]
    elif dataformat == 'CHW':
        assert crop_h <= tensor.shape[1]
        assert crop_w <= tensor.shape[2]
        x = np.random.randint(0, tensor.shape[1] - crop_h)  # row
        y = np.random.randint(0, tensor.shape[2] - crop_w)  # column
        tensor = tensor[:, :, x:x+crop_h, y:y+crop_w]

    return tensor


# **************************************************
# ***************** Train and test *****************
# **************************************************
def lr_scheduler(warmup_end=0, lr_schedule='liner', step_size=1, gamma=0.95, epochs=100, final_multiplier=0.001):
    """
    返回一个函数用于作为参数传入 `torch.optim.lr_scheduler.LambdaLR` 以控制学习率.
    该函数根据step得到一个系数,然后该系数直接与`init_LR`相乘.

    Args:

        epochs(int) - Max epochs.

        warmup_end - End epoch of warmup

        lr_schedule - Schedule of learning rate change straigt
            'step' - Sets LR to the init_lr decayed by gamma every step_size epochs.
                step_size (int) - Period of learning rate decay.
                gamma (float) - Multiplicative factor of learning rate decay.
            'linear' -
            'cosine' -
    考虑使用torch.optim.lr_scheduler下的LambdaLR包装
    """
    def _lr_step_policy(last_epoch):
        last_epoch = last_epoch // step_size
        if last_epoch < warmup_end:
            lr = (last_epoch + 1) / warmup_end  # warmup
        else:
            if last_epoch == 0:
                lr = 1
            else:
                lr = gamma**(last_epoch - warmup_end)
        return lr

    def _lr_linear_policy(last_epoch):
        if last_epoch < warmup_end:
            lr = (last_epoch + 1) / warmup_end  # warmup
        else:
            e = last_epoch - warmup_end
            es = epochs - warmup_end
            lr = 1 - (e / es)
        return lr

    def _lr_cosine_policy(last_epoch):
        if last_epoch < warmup_end:
            lr = (last_epoch + 1) / warmup_end  # warmup
        else:
            e = last_epoch - warmup_end
            es = epochs - warmup_end
            lr = 0.5 * (1 + np.cos(np.pi * e / es))
        return lr

    def _lr_exponential_policy(last_epoch):
        es = epochs - warmup_end
        epoch_decay = np.power(2, np.log2(final_multiplier)/es)

        if last_epoch < warmup_end:
            lr = (last_epoch + 1) / warmup_end  # warmup
        else:
            e = last_epoch - warmup_end
            lr = epoch_decay ** e
        return lr

    if lr_schedule == 'step':
        return _lr_step_policy
    elif lr_schedule == 'linear':
        return _lr_linear_policy
    elif lr_schedule == 'cosine':
        return _lr_cosine_policy
    elif lr_schedule == 'exponential':
        return _lr_exponential_policy


class _LRScheduler(object):

    def __init__(self, optimizer, last_epoch=-1):
        if not isinstance(optimizer, torch.optim.Optimizer):
            raise TypeError('{} is not an Optimizer'.format(
                type(optimizer).__name__))
        self.optimizer = optimizer
        if last_epoch == -1:
            for group in optimizer.param_groups:
                group.setdefault('initial_lr', group['lr'])
            last_epoch = 0
        else:
            for i, group in enumerate(optimizer.param_groups):
                if 'initial_lr' not in group:
                    raise KeyError("param 'initial_lr' is not specified "
                                   "in param_groups[{}] when resuming an optimizer".format(i))
        self.base_lrs = list(map(lambda group: group['initial_lr'], optimizer.param_groups))
        self.step(last_epoch)

    def get_lr(self):
        raise NotImplementedError

    def step(self, epoch=None):
        if epoch is None:
            epoch = self.last_epoch + 1
        self.last_epoch = epoch
        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group['lr'] = lr * self.ext_coefficient


class LambdaWarmLR(_LRScheduler):
    """ Modify from torch.optim.LambdaLR
    Sets the learning rate of each parameter group to the initial lr
    times a given function. When last_epoch=-1, sets initial lr as lr.

    Args:
        optimizer (Optimizer): Wrapped optimizer.
        lr_lambda (function or list): A function which computes a multiplicative
            factor given an integer parameter epoch, or a list of such
            functions, one for each group in optimizer.param_groups.
        last_epoch (int): The index of last epoch. Default: -1.

    Example:
        >>> # Assuming optimizer has two groups.
        >>> lambda1 = lambda epoch: epoch // 30
        >>> lambda2 = lambda epoch: 0.95 ** epoch
        >>> scheduler = LambdaLR(optimizer, lr_lambda=[lambda1, lambda2])
        >>> for epoch in range(100):
        >>>     train(...)
        >>>     validate(...)
        >>>     scheduler.step()
    """

    def __init__(self, optimizer, lr_lambda, last_epoch=-1):
        self.optimizer = optimizer
        if not isinstance(lr_lambda, list) and not isinstance(lr_lambda, tuple):
            self.lr_lambdas = [lr_lambda] * len(optimizer.param_groups)
        else:
            if len(lr_lambda) != len(optimizer.param_groups):
                raise ValueError("Expected {} lr_lambdas, but got {}".format(
                    len(optimizer.param_groups), len(lr_lambda)))
            self.lr_lambdas = list(lr_lambda)
        self.last_epoch = last_epoch
        self.ext_coefficient = 1
        super(LambdaWarmLR, self).__init__(optimizer, last_epoch)

    def get_lr(self):
        return [base_lr * lmbda(self.last_epoch)
                for lmbda, base_lr in zip(self.lr_lambdas, self.base_lrs)]


class DataPrefetcher():
    def __init__(self, loader, opt):
        self.loader = iter(loader)
        self.opt = opt
        self.stream = torch.cuda.Stream()
        # With Amp, it isn't necessary to manually convert data to half.
        # if args.fp16:
        #     self.mean = self.mean.half()
        #     self.std = self.std.half()
        self.preload()

    def preload(self):
        try:
            self.next_batch = next(self.loader)
        except StopIteration:
            self.next_batch = None
            return
        # with torch.cuda.stream(self.stream):
        #     for k in self.next_batch:
        #         if k != 'meta':
        #             self.next_batch[k] = self.next_batch[k].to(device=self.opt.gpu, non_blocking=True)

            # With Amp, it isn't necessary to manually convert data to half.
            # if args.fp16:
            #     self.next_input = self.next_input.half()
            # else:
            #     self.next_input = self.next_input.float()

    def next(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        next_batch = self.next_batch
        self.preload()
        return next_batch


def test_time_augment(net, image, mode='cls'):
    """ Do test time augmentations on image(s) for classification or segmentation.

    Args:
        image: [N, C, H, W] tensor of image (have transformed)
        mode: 'cls' for classification, 'seg' for segmentation.

    """
    # predict a complete image
    n, c, h, w = image.shape

    aug_imgs = []
    for i in range(4):
        aug_imgs.append(torch.rot90(image.clone(), i, dims=(3, 2)))
    aug_imgs.append(torch.flip(image.clone(), [2]))  # filp H
    aug_imgs.append(torch.flip(image.clone(), [3]))  # filp H
    aug_imgs = torch.stack(aug_imgs, dim=0).view(-1, c, h, w)
    with torch.no_grad():
        outputs = net(aug_imgs)
    outputs = outputs.view(6, n, -1, h, w)
    if mode == 'cls':
        predict = outputs.mean(dim=0)  # [6,N,C] → [N,C]
    elif mode == 'seg':
        # outputs: [NCHW]
        predict = torch.flip(outputs[5], [3])
        predict += torch.flip(outputs[4], [2])
        for i in range(4):
            predict += torch.rot90(outputs[i], i, dims=(2, 3))

    return predict


def pre_a_big_img_tta(net, image, opt, crop_info, device=None, tta=False):
    """Predict a list of images slide cropped from a big image (with `test_time_augment`),
    and `vote_combine` results, then return a entire big predict label.
    Args:
        net: Trained model
        image: A big image to be predicted
        opt: An instance of config class(including size, crop_params, etc.)
        crop_info: [rows, cols]
            rows: Num of images in the row direction.
            cols: Num of images in the col direction.
        tta: (bool) if use `test_time_augment` for predict
    Return:
        predict: [HWC] array, where C is the num of classes
    """
    predict = []
    image = image.squeeze(dim=0)  # [NLCHW] -> [LCHW]
    with torch.no_grad():
        if image.shape[0] <= opt.bs:
            if tta:
                output = test_time_augment(net, image.to(device), 'seg')
            else:
                output = net(image.to(device))
            if opt.input_size[0] != opt.crop_params[0]:
                output = F.interpolate(
                    output, size=opt.crop_params[:2], mode='nearest')
            output = np.transpose(output.cpu().numpy(), (0, 2, 3, 1))  # [LCHW]->[LHWC]
            predict += list(output)  # TODO: test
        else:
            inds = 0
            while inds < image.shape[0]:
                # torch.cuda.empty_cache()
                inde = min(inds + opt.bs, image.shape[0])
                input = image[inds: inde, :, :, :]
                if tta:
                    output = test_time_augment(net, input.to(device), 'seg')
                else:
                    output = net(input.to(device))
                if opt.input_size[0] != opt.crop_params[0]:
                    output = F.interpolate(
                        output, size=opt.crop_params[:2], mode='nearest')
                output = np.transpose(output.cpu().numpy(), (0, 2, 3, 1))  # [LCHW]->[LHWC]
                predict += list(output)
                inds = inde
    predict = vote_combine(predict, opt.crop_params, crop_info, 2)
    predict = F.softmax(F.normalize(torch.from_numpy(predict), dim=-1), dim=-1)
    return predict.numpy()


# **************************************************
# ***************** Pt model utils *****************
# **************************************************
def update_params(target_net, ref_net, block_layers=[]):
    block_layers = [block_layers] if type(block_layers) is str else block_layers

    target_dict = target_net.state_dict()
    ref_dict = ref_net.state_dict()
    tar_k_type = 1 if 'module' in list(target_dict.keys())[0] else 0
    ref_k_type = 1 if 'module' in list(ref_dict.keys())[0] else 0

    temp_dict = {}  # 中转
    for k_ref, v_ref in ref_dict.items():
        if tar_k_type == ref_k_type:
            k_tar = k_ref
        elif tar_k_type and not ref_k_type:
            k_tar = 'module.' + k_ref
        elif not tar_k_type and ref_k_type:
            k_tar = k_ref[len('module.'):]

        if k_tar in target_dict:
            if len(block_layers) > 0:
                if any(bl_l in k_tar for bl_l in block_layers):
                    print('Block_layer:\t %s' % k_tar)
                    continue
            temp_dict[k_tar] = v_ref

    target_dict.update(temp_dict)
    target_net.load_state_dict(target_dict)
    return target_net


def load_ckpt(model, ckpt, train=False, block_layers=[], map_loc=None, vis=None):
    ''' Load ckpt and setup some state. '''
    # print("Trying to load model")
    if os.path.isfile(ckpt):
        if map_loc is None:
            map_loc = None if torch.cuda.is_available() else 'cpu'
        block_layers = [block_layers] if type(block_layers) is str else block_layers
        model_dict = model.state_dict()
        pretrained_dict = torch.load(ckpt, map_location=map_loc)
        print('Load ckpt info:')
        print('\tModel parameters count: %d' % (len(list(model_dict.keys()))))
        print('\tCp parameters count: %d' % (len(list(pretrained_dict.keys()))))
        # 剔除由于 torch.nn.DataParallel 包装而增多的key
        if 'module' in list(pretrained_dict.keys())[0]:
            if 'module' not in list(model_dict.keys())[0]:
                new_dict = {}
                for k, v in pretrained_dict.items():
                    new_dict[k[len('module.'):]] = v
                pretrained_dict = new_dict
        if 'module' in list(model_dict.keys())[0]:
            if 'module' not in list(pretrained_dict.keys())[0]:
                new_dict = {}
                for k, v in pretrained_dict.items():
                    new_dict['module.'+k] = v
                pretrained_dict = new_dict

        if len(block_layers) > 0:
            filtered_dict = {}
            bl_count = 0
            for k, v in pretrained_dict.items():
                if any(bl_l in k for bl_l in block_layers):
                    # print('Block_layer:\t %s' % k)
                    bl_count += 1
                    continue
                filtered_dict[k] = v
            model_dict.update(filtered_dict)
            print('\tBlock layer names: {}\n\tBlock parameters count: {}.'.format(block_layers, bl_count))
        else:
            model_dict = pretrained_dict
        model.load_state_dict(model_dict)

        print('\tLoad checkpoint file (%s).' % ckpt)
    else:
        if train:
            print('\tCheckpoint file (%s) is not exist, re-initializtion' % ckpt)
        else:
            raise ValueError('Failed to load model checkpoint (%s).' % ckpt)
    return model


def save_ckpt(model, ckpt='cp', filename='checkpoint'):
    ''' Save checkpoint.
    Args:
        ckpt - Dir of ckpt to save.
        filename - Only name of ckpt to save.
    '''
    # import shutil
    filepath = ckpt+'/'+filename+'.pth'
    if type(model) in [torch.nn.DataParallel, torch.nn.parallel.DistributedDataParallel]:
        model_dict = model.module.state_dict()
    else:
        model_dict = model.state_dict()
    torch.save(model_dict, filepath)


def clean_ckpt(root, keep_ids, delete=False):
    trash_dir = os.path.dirname(root) + '/Trash'
    if not os.path.exists(trash_dir):
        os.mkdir(trash_dir)

    print('Cleaning ckpts in "{}"'.format(root))
    cp_list = sorted(os.listdir(root))
    drop_cp_num = 0
    for ckpt in cp_list:
        cur_id = ckpt.split('_')[1]
        if cur_id not in keep_ids:
            drop_cp_num += 1
            if delete:
                print('\tDel {}'.format(ckpt))
                os.remove(root + '/' + ckpt)
            else:
                print('\tTrash {}'.format(ckpt))
                shutil.move(root + '/' + ckpt, trash_dir + '/' + ckpt)

    operation_str = 'deleted' if delete else 'trashed to {}'.format(trash_dir)
    print('A total of {:d} ckpts were {}.'.format(drop_cp_num, operation_str))


def count_params(net):
    ''' Count total params of network'''
    print('Total params: %.2fM' %
          (sum(p.numel() for p in net.parameters()) / 1000000.0))


def prep_param_lists(model):
    model_params = [p for p in model.parameters() if p.requires_grad]
    master_params = [p.clone().detach().float() for p in model_params]

    for p in master_params:
        p.requires_grad = True


def get_last_conv_name(net):
    """
    获取网络的最后一个卷积层的名字
    :param net:
    :return:
    """
    layer_name = None
    for name, m in net.named_modules():
        if isinstance(m, torch.nn.Conv2d):
            layer_name = name
    return layer_name


# **************************************************
# *************** Some Implements ******************
# **************************************************
class LARS(torch.optim.Optimizer):
    r"""Implements layer-wise adaptive rate scaling for SGD.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): base learning rate (\gamma_0)
        momentum (float, optional): momentum factor (default: 0) ("m")
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
            ("\beta")
        eta (float, optional): LARS coefficient
        max_epoch: maximum training epoch to determine polynomial LR decay.

    Based on Algorithm 1 of the following paper by You, Gitman, and Ginsburg.
    Large Batch Training of Convolutional Networks:
        https://arxiv.org/abs/1708.03888

    Example:
        >>> optimizer = LARS(model.parameters(), lr=0.1, eta=1e-3)
        >>> optimizer.zero_grad()
        >>> loss_fn(model(input), target).backward()
        >>> optimizer.step()
    """
    def __init__(self, params, lr=1e-3, momentum=.9,
                 weight_decay=.0005, eta=0.001, max_epoch=200):
        if lr < 0.0:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if momentum < 0.0:
            raise ValueError("Invalid momentum value: {}".format(momentum))
        if weight_decay < 0.0:
            raise ValueError("Invalid weight_decay value: {}"
                             .format(weight_decay))
        if eta < 0.0:
            raise ValueError("Invalid LARS coefficient value: {}".format(eta))

        self.epoch = 0
        defaults = dict(lr=lr, momentum=momentum,
                        weight_decay=weight_decay,
                        eta=eta, max_epoch=max_epoch)
        super(LARS, self).__init__(params, defaults)

    def step(self, epoch=None, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
            epoch: current epoch to calculate polynomial LR decay schedule.
                   if None, uses self.epoch and increments it.
        """
        loss = None
        if closure is not None:
            loss = closure()

        if epoch is None:
            epoch = self.epoch
            self.epoch += 1

        for group in self.param_groups:
            weight_decay = group['weight_decay']
            momentum = group['momentum']
            eta = group['eta']
            lr = group['lr']
            max_epoch = group['max_epoch']

            for p in group['params']:
                if p.grad is None:
                    continue

                param_state = self.state[p]
                d_p = p.grad.data

                weight_norm = torch.norm(p.data)
                grad_norm = torch.norm(d_p)

                # Global LR computed on polynomial decay schedule
                decay = (1 - float(epoch) / max_epoch) ** 2
                global_lr = lr * decay

                # Compute local learning rate for this layer
                local_lr = eta * weight_norm / (grad_norm + weight_decay * weight_norm)

                # Update the momentum term
                actual_lr = local_lr * global_lr

                if 'momentum_buffer' not in param_state:
                    buf = param_state['momentum_buffer'] = torch.zeros_like(p.data)
                else:
                    buf = param_state['momentum_buffer']
                buf.mul_(momentum).add_(actual_lr, d_p + weight_decay * p.data)
                p.data.add_(-buf)

        return loss
