'''
深度学习基础工具
'''
import os
# import sys
# import datetime
import torch
import numpy as np
# import random
import psutil
import shutil
import matplotlib.pyplot as plt


# **********************************************
# **************** Setup Cuda ******************
# **********************************************
def setup_mode(if_gpu,
               gpu_id='0',
               cudnn_benchmark=True):
    ''' Set up basic mode for training. '''
    from torch.backends import cudnn

    if torch.cuda.is_available() and if_gpu:
        # 让内置的cuDNN的auto-tuner自动寻找最适合当前配置的高效算法，以优化效率
        cudnn.benchmark = cudnn_benchmark
        # cudnn.deterministic = True
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id  # 指定运行GPU
        device = torch.device('cuda')

        # 专治：RuntimeError: CUDA error: unknown error
        # torch.cuda.current_device()
        pin_memory = True
        print('Use device: ', device)
        print('GPU Mode')
    else:
        device = torch.device("cpu")
        pin_memory = False
        print('CPU Mode')

    return device, pin_memory


class CudaDevices():
    """ A simple class to know about your cuda devices

    Args:
        param1:  param1 specification

    Attributes:
        self.gpu_num (int): Total GPU num
        self.avail_num (int): Available GPU num (memory occupied < 100M)
        self.avail_ids (list of int): Available GPU Id.

    """
    def __init__(self, ):
        self.gpu_num = torch.cuda.device_count()  # Total GPU num
        self.avail_ids = []
        print("%d device(s) found:" % self.gpu_num)
        for i in range(self.gpu_num):
            memory_occupied = torch.cuda.memory_allocated(i) / 1024 / 1024
            print('\t%s (Id %d): current GPU memory occupied = %.2f M' % (
                torch.cuda.get_device_name(i), i, memory_occupied))
            if memory_occupied < 100:
                self.avail_ids.append(i)

        self.avail_num = len(self.avail_ids)

        print('Total GPU num = %d, availiable GPU num = %d' % (
            self.gpu_num, self.avail_num))

    def total_gpu(self):
        """返回 cuda 设备的总数量"""
        return torch.cuda.device_count()

    def total_ids_str(self):
        '''以 a string 返回所有设备ids'''
        num = torch.cuda.device_count()
        if num > 0:
            ids = ''
            for i in range(num):
                ids += str(i) + ','
            return ids[:-1]
        else:
            return None

    def total_ids_list(self):
        '''以 list of int 形式返回所有设备ids'''
        num = torch.cuda.device_count()
        if num > 0:
            return [i for i in range(num)]
        else:
            return None

    def avail_ids_str(self):
        '''以 a string 返回可用设备ids'''
        if len(self.avail_ids) > 0:
            ids = ''
            for i in self.avail_ids:
                ids += str(i) + ','
            return ids[:-1]
        else:
            return None

    def avail_ids_list(self):
        '''以 list of int 形式返回可用设备ids'''
        if self.avail_num > 0:
            return [i for i in range(self.avail_num)]
        else:
            return None

    def devices(self, vis=None):
        """获取所有可用的设备的名称"""
        self.gpu_num = torch.cuda.device_count()
        self.avail_ids = []
        log_str = ''
        log_str += "%d device(s) found:\n" % self.gpu_num
        for i in range(self.gpu_num):
            memory_occupied = torch.cuda.memory_allocated(i) / 1024 / 1024
            log_str += '\t%s (Id %d): current GPU memory occupied = %.2f M\n' % (
                torch.cuda.get_device_name(i), i, memory_occupied)
            if memory_occupied < 100:
                self.avail_ids.append(i)

        self.avail_num = len(self.avail_ids)
        log_str += 'Total GPU num = %d, availiable GPU num = %d\n' % (
            self.gpu_num, self.avail_num)

        if vis is not None:
            vis.log('\n' + log_str, if_print=True)
        else:
            print(log_str)


# **********************************************
# *************** Useful tools *****************
# **********************************************
def backup_codes(src_dir, dst_dir, kind='py', exclude_str=[]):
    exclude_str += ['__pycache__', '.vscode', 'run', 'wandb', 'Bash', 'Log', 'BackUp']
    for folder, subfolders, files in os.walk(src_dir):
        if any(bl in folder for bl in exclude_str):
            continue
        folder = folder.replace(os.getcwd(), '')
        folder = folder.lstrip('\\')
        folder = folder.lstrip('/')
        for file in files:
            if(file.endswith('.'+kind)):
                src_pth = os.path.join(folder, file)
                dst_pth = os.path.join(dst_dir, src_pth)
                dst_folder = os.path.dirname(dst_pth)
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                shutil.copy(src_pth, dst_pth)


# **************************************************
# ************ Performance monitoring **************
# **************************************************
def do_cprofile(filename):
    """ 性能分析装饰器定义
    Decorator for function profiling.
    """
    import cProfile
    import pstats

    def wrapper(func):
        def profiled_func(*args, **kwargs):
            # Flag for do profiling or not.
            DO_PROF = os.getenv("PROFILING")
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper


class MemoryInfo():
    """ A simple class to know about your memory information.

    Args:
        unit: 'M' or 'G'

    Attributes:
        self.total_memo (float): Total memory
    """
    def __init__(self, unit='M'):

        self.unit = unit.upper()
        self.den = float({'M': 2**20, 'G': 2**30}[self.unit])

        self.memo = psutil.virtual_memory()
        self.total_memo = self.memo.total / self.den
        print('Total Memory: %.2f %s' % (self.total_memo, self.unit))

    def cur_memo(self):
        occpied_memo = psutil.Process(os.getpid()).memory_info().rss / self.den
        print('Memory occpied: {:.2f} {} ({:.2%})\n'.format(
            occpied_memo, self.unit, occpied_memo/self.total_memo))
        return occpied_memo

    def cur_memo_info(self, vis=False):
        """ Return the string info about current occpied memory.
        """
        occpied_memo = psutil.Process(os.getpid()).memory_info().rss / self.den
        memo_info_str = 'Memory occpied: {:.2f} {} ({:.2%})\n'.format(
            occpied_memo, self.unit, occpied_memo/self.total_memo)
        if vis:
            print(memo_info_str)
        return memo_info_str


# **********************************************
# **********  Result visualization  ************
# **********************************************
def visualize_feature_map(FM, outdir, num=1, name=None):
    '''
    Parse the input FeatureMap and do sample visualization
    Args:
        input: Tensor of feature map.
        outdir: Dir of ouput image saving.

    '''
    FM = np.array(FM)
    if len(FM.shape) == 5:  # [11HWC] -> [1HWC]
        FM = FM[0]
    if len(FM.shape) == 4:  # [1HWC] -> [HWC]
        FM = FM[0]

    h, w, c = FM.shape
    # 归一化 0-1
    tp_min, tp_max = np.min(FM), np.max(FM)
    if tp_min < 0:
        FM += abs(tp_min)
    FM /= (tp_max - tp_min)

    # Iterate filters
    for i in range(c):
        fig = plt.figure(figsize=(12, 12))
        axes = fig.add_subplot(111)
        img = FM[:, :, i]
        # Toning color
        axes.imshow(img, vmin=0, vmax=0.9, interpolation='bicubic', cmap='coolwarm')
        # Remove any labels from the axes
        # axes.set_xticks([])
        # axes.set_yticks([])

        # Save figure
        if name is None:
            # misc.imsave(outdir + '/%d_%.3d.png' % (num, i), FM[:, :, i])
            plt.savefig(outdir + '/%d_%.3d.png' % (num, i), dpi=60, bbox_inches='tight')
        else:
            # misc.imsave(outdir + '/%s_%.3d.png' % (name, i), FM[:, :, i])
            plt.savefig(outdir + '/%s_%.3d.png' % (name, i), dpi=60, bbox_inches='tight')
        plt.close(fig)


if __name__ == '__main__':
    # in_dir = '/home/tao/Data/VOCdevkit2007/VOC2007/small/train'
    # rename_files(in_dir)
    # mkdir_of_dataset('/home/tao/Data/XM')
    pass
