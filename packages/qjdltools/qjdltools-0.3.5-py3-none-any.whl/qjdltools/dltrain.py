"""
Tools collection of operations during training.
The icluded functions are:
    def train_log()
    def memory_watcher()
    def Accuracy Evaluation[serval functions]

Version 1.0  2018-04-02 22:44:32
    by QiJi Refence: https://github.com/GeorgeSeif/Semantic-Segmentation-Suite
Version 2.0  2018-10-29 09:10:41 by QiJi
Version 3.0  2019-12-12 16:40:46 by QiJi
    1. The naming of each indicator is standardized according to `sklearn.metrics`.
    2. The calculation speed is optimized
    3. Evaluation indicators are printed in markdown format
Version 4.0  2020-04-02 14:43:56 by QiJi
    1. Evaluation - support multi-label evaluation
    2. Add LR Schedler functions
"""
import datetime
# import os
import math
import sys
import torch

import numpy as np
from skimage import morphology
# from sklearn import metrics
# from matplotlib import pyplot as plt


def train_log(X, prefix='', f=None):
    """ Print with time. To console or a file(f) """
    time_stamp = datetime.datetime.now().strftime("[%d %H:%M:%S]")
    if f is not None:
        if type(f) == str:
            with open(f, 'a') as f:
                f.write(time_stamp + " " + X)
        else:
            f.write(time_stamp + " " + X)

    sys.stdout.write(prefix + time_stamp + " " + X)
    sys.stdout.flush()


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


# **********************************************
# ************** LR Schedler *******************
# **********************************************
def adjust_learning_rate(optimizer, cepoch, args, lr=None):
    """Decay the learning rate based on schedule"""
    lr = args.lr if lr is None else lr

    def _cal_coefficient(epoch):
        if epoch < args.warmup:
            coefficient = (epoch + 1) / args.warmup  # warmup
        else:
            if args.lr_policy == 'cosine':  # cosine lr schedule
                coefficient = 0.5 * (1. + math.cos(math.pi * epoch / args.mepoch))
            elif args.lr_policy == 'linear':
                coefficient = 1 - (epoch-args.warmup) / (args.mepoch-args.warmup)
            elif args.lr_policy == 'step':  # stepwise lr schedule
                for milestone in args.milestones:
                    coefficient = args.lr_decay[1] if epoch >= milestone else 1.
            elif args.lr_policy == 'polyline':  # stepwise lr schedule
                if epoch > args.milestones[0]:
                    # start decay
                    coefficient = (args.mepoch - epoch)/(args.mepoch - args.milestones[0])
        return coefficient

    last_epoch = max(1, cepoch-1)
    last_coeff = _cal_coefficient(last_epoch)
    cur_coeff = _cal_coefficient(cepoch)
    for param_group in optimizer.param_groups:
        base_lr = param_group['lr'] / last_coeff
        new_lr = base_lr * cur_coeff
        param_group['lr'] = new_lr

    return lr * cur_coeff  # main base lr (no hos)


# **********************************************
# *************** Evaluation *******************
# **********************************************
def fast_hist(y_true, y_pred, n_class):
    """ Computational confusion matrix.
    -------------------------------------------
    |          | p_cls_1 | p_cls_2 |   ....   |
    -------------------------------------------
    | gt_cls_1 |         |         |          |
    -------------------------------------------
    | gt_cls_2 |         |         |          |
    -------------------------------------------
    |   ....   |         |         |          |
    -------------------------------------------
    """
    # mask = (y_true >= 0) & (y_true < n_class)
    if len(y_true.shape) > 1:
        y_true = y_true.flatten()
        y_pred = y_pred.flatten()
    hist = np.bincount(
        n_class * y_true.astype(int) + y_pred,
        minlength=n_class ** 2, ).reshape(n_class, n_class)
    return hist


def fast_hist_multilabel(y_true, y_pred, n_class):
    """Compute serval confusion matrixs for each class.
    Args:
        y_true, y_pred (ndarray): shape of [sample_num, classes_num]

    Returns: confusion matrix ndarray
        The num of hist matrixs is `n_class`. Each hist matrix is shown as following:
            --------------------------------
            |                |  Predicted  |
            -    Class_i     ---------------
            |                |   0  |   1  |
            --------------------------------
            |         |  0   |  TN  |  FP  |
            -   GT    ----------------------
            |         |  1   |  FN  |  TP  |
            --------------------------------
        Briefly, it is shown as:
            ---------------
            |  TN  |  FP  |
            ---------------
            |  FN  |  TP  |
            ---------------
    """
    multi_hist = []
    for c in range(n_class):
        y_t, y_p = y_true[:, c], y_pred[:, c]
        hist = np.bincount(
            2 * y_t.astype(int) + y_p,
            minlength=2 ** 2,).reshape(2, 2)
        multi_hist.append(hist)
    return np.stack(multi_hist, axis=0)


def sample_evaluation(y_true, y_pred):
    """ Compute sample-wise evaluations for multi-label. """
    TP = np.array((y_true != 0) & (y_pred != 0), dtype=np.float64)
    # FP = np.array((y_true != 0) & (y_pred == 0), dtype=np.float64)
    # TN = np.array((y_true == 0) & (y_pred == 0), dtype=np.float64)
    # FN = np.array((y_true == 0) & (y_pred != 0), dtype=np.float64)

    y_pred_sum = np.sum(y_pred, 1)  # sample-wise sum of y_pred
    y_true_sum = np.sum(y_true, 1)  # sample-wise sum of y_true

    sample_precision = np.where(
        y_pred_sum == 0,
        np.zeros((y_true.shape[0])),
        np.sum(TP, 1)/y_pred_sum)

    sample_recall = np.where(
        y_true_sum == 0,
        np.zeros((y_true.shape[0])),
        np.sum(TP, 1) / y_true_sum)

    return sample_precision, sample_recall


def fbeta_score(beta, precision, recall):
    """ Compute fbeta score """
    # fscore = np.where(
    #     ((beta * beta) * precision) + recall == 0,
    #     np.zeros((precision.shape[0]), dtype=np.float64),
    #     ((1. + (beta * beta)) * (precision * recall) / ((beta * beta) * precision) + recall)
    # )
    fscore = (1.0 + (beta*beta)) * (precision * recall) / (((beta*beta) * precision) + recall + 1e-8)
    return fscore


def compute_global_accuracy(pred, label):
    """
    Compute the average segmentation accuracy across all classes,
    Input [HW] or [HWC] label
    """
    count_mat = pred == label
    return np.sum(count_mat) / np.prod(count_mat.shape)


class runingScore(object):
    """ Evaluation class.

    Args: (Specify one of the following two parameters is Ok)
        n_classes: (int) Number of categories.
        target_names: A string list of category names.
    """
    def __init__(self, n_classes=2, target_names=None):
        if target_names is None:
            self.n_classes = n_classes
            self.target_names = [str(c) for c in range(n_classes)]
        else:
            self.target_names = target_names
            self.n_classes = len(target_names)

        self.confusion_matrix = np.zeros((n_classes, n_classes), dtype=np.int64)

    def reset(self):
        """ Reset confusion_matrix. """
        self.confusion_matrix = np.zeros((self.n_classes, self.n_classes), dtype=np.int64)

    def update_all(self, y_trues, y_preds):
        """ Add new pairs of predicted label and GT label to update the confusion_matrix.
        Note: Only suitable for segmentation
        """
        for lt, lp in zip(y_trues, y_preds):
            self.confusion_matrix += fast_hist(lt, lp, self.n_classes)

    def print_hist(self, hist=None):
        """ Print the confusion matrix in markdown table style.

        Args:
            class_table: Dict of class_name and num, {'BG': 0, 'Road': 1, ...}.
            hist: Confusion_matrix array.
        """
        hist = self.confusion_matrix if hist is None else hist

        form = '|  | '
        # Form title row and second row
        for name in self.target_names:
            form += ' %s |' % name
        second_row = '| -: |' + ' -: |' * self.n_classes + '\n'
        form += '\n' + second_row

        # Rest rows
        for i in range(self.n_classes):
            form += '| %s |' % self.target_names[i]
            for j in range(self.n_classes):
                form += ' %d |' % hist[i, j]
            form += '\n'

        print(form)

    def print_score_in_md(self, score, cls_header, ave_header, digits=4):
        """ Print the score dict in markdown style. """

        form = ''
        # 1. Class-wise evaluation scores
        ind_num = len(cls_header)  # num of indicators (inducding cls names)
        title_fmt = '|  |' + ' {} |' * ind_num + ' {cat} |\n'  # Title row
        form += title_fmt.format(*cls_header, cat='category')
        form += '| -: |' + ' -: |' * (ind_num + 1) + '\n'  # Second row

        row_fmt = '| {} |' + ' {:.{digits}f}|' * ind_num + ' {} |\n'
        rows_conttents = [score[key] for key in cls_header]
        indexs = range(self.n_classes)
        rows_conttents.insert(0, indexs)  # first col is indexs
        rows_conttents.append(self.target_names)  # last col is category names
        for i, row in enumerate(zip(*rows_conttents)):
            form += row_fmt.format(*row, digits=digits)

        # Overall evaluation
        for head in ave_header:
            form += '| {} | {:.{digits}f} |\n'.format(head, score[head], digits=digits)
        print(form)

        return form


class ClassifyScore(runingScore):
    """ Accuracy evaluation for classification(multi-class)"""
    def update(self, y_true, y_pred, step_score=False):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix."""
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist
        if step_score:
            return self.get_scores(hist)

    def get_scores(self, hist=None):
        """Returns accuracy score evaluation result.
            'hist': Computational confusion matrix.

            'precision': precision of per (User accuracy)

            'recall': recall of per category  (Producer accuracy)

            'f1-score': f1-score of per category

            'OA': Overall accuracy (micro average in sklearn, averaging the
            total true positives, false negatives and false positives)

            'AA': Average accuracy (macro average in sklearn, averaging the
            unweighted mean per label)

            'Kappa': Cohen’s kappa, a statistic that measures inter-annotator agreement
        """
        hist = self.confusion_matrix if hist is None else hist

        # Class-wise evaluation
        TP = np.diag(hist)  # class-wise TP
        TPFP = hist.sum(axis=0)  # class-wise TP + FP; (row)
        TPFN = hist.sum(axis=1)  # class-wise TP + FN; (col)
        precision = TP / (TPFP + 1e-8)  # TP / (TP + FP)
        recall = TP / (TPFN + 1e-8)  # TP / (TP + FN)
        f1_score = 2 * TP / (TPFN + TPFP + 1e-8)  # 2TP / (2TP + FP + FN)

        # Overall evaluation
        n = hist.sum()
        p0 = TP.sum()

        micro_precision = p0 / (n+1e-8)  # Overall accuracy
        macro_precision = np.nanmean(precision)  # Average accuracy
        kappa = (n*p0-np.inner(TPFP, TPFN)) / (n*n - np.inner(TPFP, TPFN) + 1e-8)  # Kappa

        return ({
            "hist": hist,  # confusion matrix

            "precision": precision,
            "recall": recall,
            "f1-score": f1_score,

            "OA": micro_precision,
            "AA": macro_precision,
            "Kappa": kappa,
        })  # Return as a dictionary

    def print_score(self, score, digits=4):
        """ Print the scores in Markdown style.

        Args:
            score: A dict of all evaluation scores.
            digits: Number of digits for formatting output floating point values.
        """
        cls_header = ['precision', 'recall', 'f1-score']
        avg_header = ['OA', 'AA', 'Kappa']
        p_score = runingScore.print_score_in_md(self, score, cls_header, avg_header, digits)
        return p_score


class ClassifyScore_multi_label(object):
    """ Accuracy evaluation for classification(multi-label)

    Args: (Specify one of the following two parameters is Ok)
        n_classes: (int) Number of categories.
        target_names: A string list of category names.
    """
    def __init__(self, n_classes=2, target_names=None):
        if target_names is None:
            self.n_classes = n_classes
            self.target_names = [str(c) for c in range(n_classes)]
        else:
            self.target_names = target_names
            self.n_classes = len(target_names)

        self.confusion_matrix = np.zeros((n_classes, 2, 2), dtype=np.int64)
        self.sample_score = {'precision': np.zeros((0), dtype=np.float64),
                             'recall': np.zeros((0), dtype=np.float64)}

    def reset(self):
        """ Reset confusion_matrix. """
        self.confusion_matrix = np.zeros((self.n_classes, 2, 2), dtype=np.int64)

    def update(self, y_true, y_pred, step_score=False):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix."""
        hist = fast_hist_multilabel(y_true, y_pred, self.n_classes)  # [n_class, 2, 2]
        self.confusion_matrix += hist

        # Accum sample-wise evaluations
        sample_precision, sample_recall = sample_evaluation(y_true, y_pred)
        self.sample_score['precision'] = np.append(self.sample_score['precision'], sample_precision)
        self.sample_score['recall'] = np.append(self.sample_score['recall'], sample_recall)

        if step_score:
            return self.get_scores(
                hist, {'precision': sample_precision, 'recall': sample_recall})

    def update_all(self, y_trues, y_preds):
        """ Add new pairs of predicted label and GT label to update the confusion_matrix.
        Note: Only suitable for segmentation
        """
        for lt, lp in zip(y_trues, y_preds):
            self.confusion_matrix += fast_hist_multilabel(lt, lp, self.n_classes)

    def get_scores(self, hist=None, sample_score=None):
        """Returns accuracy score evaluation result.
            'hist': Computational confusion matrix.

            'precision': precision of per (User accuracy)

            'recall': recall of per category  (Producer accuracy)

            'f1-score': f1-score of per category

            'OA': Overall accuracy (micro average in sklearn, averaging the
            total true positives, false negatives and false positives)

            'AA': Average accuracy (macro average in sklearn, averaging the
            unweighted mean per label)

            'Kappa': Cohen’s kappa, a statistic that measures inter-annotator agreement
        """
        hist = self.confusion_matrix if hist is None else hist
        sample_score = self.sample_score if sample_score is None else sample_score

        # Sample-wise evaluation, [sample_num,]
        sample_precision = sample_score['precision']
        sample_recall = sample_score['recall']

        sample_f1_score = fbeta_score(1., sample_precision, sample_recall)

        # Class-wise evaluation, [n_class,]
        TP = hist[:, 1, 1]  # TP of per class
        TPFP = hist[:, :, 1].sum(axis=-1)  # class-wise TP + FP; (col)
        TPFN = hist[:, 1, :].sum(axis=-1)  # class-wise TP + FN; (row)

        macro_precision = TP / (TPFP + 1e-8)  # TP / (TP + FP)
        macro_recall = TP / (TPFN + 1e-8)  # TP / (TP + FN)
        # f1_score = 2 * TP / (TPFN + TPFP + 1e-8)  # 2TP / (2TP + FP + FN)

        # Overall evaluation
        # n = hist.sum()
        p0 = TP.sum()

        micro_precision = p0 / (TPFP.sum()+1e-8)  # Overall accuracy
        micro_recall = p0 / (TPFN.sum()+1e-8)  # Overall recall

        macro_precision_avg = np.nanmean(macro_precision)  # Class Average accuracy
        macro_recall_avg = np.nanmean(macro_recall)  # Class Average recall

        micro_f1_score = fbeta_score(1., micro_precision, micro_recall)
        macro_f1_score = fbeta_score(1., macro_precision, macro_recall)
        macro_f1_score_avg = np.nanmean(macro_f1_score)  # Class Average f1_score

        # kappa = (n*p0-np.inner(TPFP, TPFN)) / (n*n - np.inner(TPFP, TPFN) + 1e-8)  # Kappa

        return ({
            "hist": hist,  # confusion matrix

            "precision": macro_precision,  # class-wise precision
            "recall": macro_recall,  # class-wise recall
            "f1-score": macro_f1_score,  # class-wise f1_score
            "OA": micro_precision,  # Overall accuracy(precision)
            "AA": macro_precision_avg,  # Class average accuracy(precision)

            "sample_precision": sample_precision,
            "sample_recall": sample_recall,
            "sample_f1_score": sample_f1_score,

            "micro_precision": micro_precision,  # OA
            "micro_recall": micro_recall,
            "micro_f1_score": micro_f1_score,

            "macro_precision": macro_precision,
            "macro_precision_avg": macro_precision_avg,
            "macro_recall": macro_recall,
            "macro_recall_avg": macro_recall_avg,
            "macro_f1_score": macro_f1_score,
            "macro_f1_score_avg": macro_f1_score_avg,
            # "Kappa": kappa,
        })  # Return as a dictionary

    def print_score(self, score, digits=4):
        """ Print the scores in Markdown style.

        Args:
            score: A dict of all evaluation scores.
            digits: Number of digits for formatting output floating point values.
        """
        cls_header = ['precision', 'recall', 'f1-score']
        avg_header = ['OA', 'AA', 'micro_f1_score', 'macro_f1_score_avg']
        p_score = runingScore.print_score_in_md(self, score, cls_header, avg_header, digits)
        return p_score

    def print_hist(self, hist=None):
        """ Print the confusion matrix in markdown table style.

        Args:
            class_table: Dict of class_name and num, {'BG': 0, 'Road': 1, ...}.
            hist: Confusion_matrix array.
        """
        hist = self.confusion_matrix if hist is None else hist

        form = '|  | '
        # Form title row and second row
        for name in self.target_names:
            form += ' %s |' % name
        second_row = '| -: |' + ' -: |' * self.n_classes + '\n'
        form += '\n' + second_row

        # Rest rows
        for i in range(self.n_classes):
            form += '| %s |' % self.target_names[i]
            for j in range(self.n_classes):
                form += ' %d |' % hist[i, j]
            form += '\n'

        print(form)


class SegScore(runingScore):
    """ Accuracy evaluation for semantic segmentation(multi-class)"""
    def update(self, y_true, y_pred, step_score=False):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix."""
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist
        if step_score:
            return self.get_scores(hist)

    def get_scores(self, hist=None):
        """Use the confusion_matrix to do evaluation.

        Returns accuracy score evaluation result:
            'hist': Computational confusion matrix.

            'precision': precision of per (User accuracy)

            'recall': recall of per category  (Producer accuracy)

            'f1-score': f1-score of per category

            'iou': IoU for per category

            'OA': Overall accuracy (micro average in sklearn, averaging the
            total true positives, false negatives and false positives)

            'AA': Average accuracy (macro average in sklearn, averaging the
            unweighted mean per label)

            'Kappa': Cohen’s kappa, a statistic that measures inter-annotator agreement

            'Mean IoU': Mean IoU

            'FWIoU': Frequency Weighted IoU
        """
        hist = self.confusion_matrix if hist is None else hist

        # Class-wise evaluation
        ep = np.ones((hist.shape[0])) * 1e-8
        TP = np.diag(hist)  # class-wise TP
        TPFP = hist.sum(axis=0)  # class-wise TP + FP; (row)
        TPFN = hist.sum(axis=1)  # class-wise TP + FN; (col)

        precision = TP / (TPFP + 1e-8)  # TP / (TP + FP)
        recall = TP / (TPFN + 1e-8)  # TP / (TP + FN)
        f1_score = 2 * TP / (TPFN + TPFP + 1e-8)  # 2TP / (2TP + FP + FN)
        iou = TP / (TPFP + TPFN - TP + ep)  # TP / (TP + FP + FN)

        # Overall evaluation
        n = hist.sum()
        p0 = TP.sum()

        micro_precision = p0 / (n+1e-8)  # Overall accuracy
        macro_precision = np.nanmean(precision)  # Average accuracy
        kappa = (n*p0-np.inner(TPFP, TPFN)) / (n*n - np.inner(TPFP, TPFN) + 1e-8)
        macro_iou = np.nanmean(iou)  # mean IoU

        # Frequency Weighted IoU(FWIoU) 根据每个类出现的频率为其设置权重
        cls_weight = hist.sum(axis=1) / (hist.sum()+1e-8)
        # fw_iou0 = (cls_weight[cls_weight > 0] * iou[cls_weight > 0]).sum()
        fw_iou = np.average(iou, weights=cls_weight)

        return ({
            "hist": hist,  # confusion matrix

            "precision": precision,
            "recall": recall,
            "f1-score": f1_score,
            "iou": iou,

            "OA": micro_precision,
            "AA": macro_precision,
            "Kappa": kappa,
            "Mean IoU": macro_iou,
            "FWIoU": fw_iou,
        })  # Return as a dictionary

    def print_score(self, score, digits=4):
        """ Print the scores in Markdown style.

        Args:
            score: A dict of all evaluation scores.
            digits: Number of digits for formatting output floating point values.
        """
        cls_header = ['precision', 'recall', 'f1-score', 'iou']
        avg_header = ['OA', 'AA', 'Kappa', 'Mean IoU', 'FWIoU']
        p_score = runingScore.print_score_in_md(self, score, cls_header, avg_header, digits)
        return p_score


class RoadExtractionScore(runingScore):
    """Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    """

    def update(self, y_true, y_pred):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix. """
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist
        return self.get_scores(hist)

    def add(self, y_true, y_pred):
        """Add a new pair of predicted label and GT label,
        update the confusion_matrix. """
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist

    def get_scores(self, hist=None):
        """Returns accuracy score evaluation result.
            - 1. Precision{ TP / (TP+FP) }
            - 2. Recall{ TP / (TP+FN) }
            - 3. F1score
            - 4. Class IoU
            - 5. Mean IoU
            - 6. FreqW Acc
        """
        hist = self.confusion_matrix if hist is None else hist

        # Take class 1-road as postive class:
        TP = hist[1, 1]  # Ture Positive(road pixels are classified into road class)
        FN = hist[1, 0]  # False Negative(road pixels are classified into bg class)
        FP = hist[0, 1]  # False Positive(bg pixels are classified into road class)
        # TN = hist[0, 0]  # Ture Negative(bg pixels are classified into bg class)

        prec = TP / (TP + FP + 1e-8)  # Precision
        rec = TP / (TP + FN + 1e-8)  # Recall
        F1 = 2*TP / (2*TP + FP + FN + 1e-8)  # F1 Score

        # IoU (tested)
        cls_iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
        mean_iu = np.nanmean(cls_iu)
        # Frequency Weighted IoU(FWIoU) 根据每个类出现的频率为其设置权重
        freq = hist.sum(axis=1) / (hist.sum()+1e-8)
        fwavacc = (freq[freq > 0] * cls_iu[freq > 0]).sum()
        # cls_iu = dict(zip(range(self.n_classes), iu))

        return (
            {
                'Precision': prec,
                'Recall': rec,
                'F1score': F1,
                'Class IoU': cls_iu,
                'Mean IoU': mean_iu,
                'FreqW Acc': fwavacc,
            }  # Return as a dictionary
        )

    def keys(self):
        score_keys = [
            'Precision,Recall,F1score,Class IoU,Class IoU,Mean IoU,FreqW Acc'
        ]  # note 'Class IoU'
        return score_keys


class RelaxedRoadExtractionScore(runingScore):
    """Relax Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    """
    def __init__(self, rho=1):
        self.rho = rho*2 + 1
        self.confusion_matrix_p = np.zeros((2, 2), np.int64)  # For relaxed precision
        self.confusion_matrix_r = np.zeros((2, 2), np.int64)  # For relaxed recall

    def update(self, y_true, y_pred):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix."""
        if self.rho > 1:
            selem = morphology.square(self.rho, dtype=y_true.dtype)
            tp_label_true = morphology.dilation(y_true, selem)
            tp_label_pred = morphology.binary_dilation(y_pred, selem)
            hist1 = fast_hist(tp_label_true, y_pred, 2)
            hist2 = fast_hist(y_true, tp_label_pred, 2)
        else:
            hist = fast_hist(y_true, y_pred, 2)
            hist1, hist2 = hist, hist

        self.confusion_matrix_p += hist1
        self.confusion_matrix_r += hist2
        return self.get_scores(hist1, hist2)

    def add(self, y_true, y_pred):
        """ Add new pairs of predicted label and GT label to update the confusion_matrix. """
        if self.rho > 0:
            selem = morphology.square(self.rho, dtype=np.int64)
            tp_lt = morphology.binary_dilation(y_true, selem)
            tp_lp = morphology.binary_dilation(y_pred, selem)
            self.confusion_matrix_p += fast_hist(tp_lt, y_pred, 2)
            self.confusion_matrix_r += fast_hist(y_true, tp_lp, 2)
        else:
            hist = fast_hist(y_true, y_pred, 2)
            self.confusion_matrix_p += hist
            self.confusion_matrix_r += hist

    def get_scores(self, hist_p=None, hist_r=None):
        hist_p = self.confusion_matrix_p if hist_p is None else hist_p
        hist_r = self.confusion_matrix_r if hist_r is None else hist_r

        prec = hist_p[1, 1] / (hist_p[1, 1] + hist_p[0, 1] + 1e-8)  # Precision
        rec = hist_r[1, 1] / (hist_r[1, 1] + hist_r[1, 0] + 1e-8)  # Recall
        f1 = 2 * prec * rec / (prec + rec + 1e-8)
        return (
            {
                "Precision": prec,
                "Recall": rec,
                "F1score": f1
            }  # Return as a dictionary
        )

    def reset(self):
        """ Reset confusion_matrixs. """
        self.confusion_matrix_p = np.zeros((2, 2), dtype=np.int64)
        self.confusion_matrix_r = np.zeros((2, 2), dtype=np.int64)


# **********************************************
# ***********                     **************
# **********************************************
def test():
    import cv2
    # from sklearn import metrics
    # from .dlimage
    # Test confusion_matrix
    # n_class = 2
    gt_pth = r'D:\Data_Lib\Seg\GLCC\hubei2D_5m\Small_dataset\Org\val_lbl\NH49E002022.tif'
    gt = cv2.imread(gt_pth, -1).flatten()

    pre_pth = r'D:\Data_Lib\Seg\GLCC\hubei2D_5m\Small_dataset\Org\val_lbl\NH49E003023.tif'
    pre = cv2.imread(pre_pth, -1).flatten()

    table = [
        "BG", "GengDi", "ChenZhen", "NongCun", "ShuiTi",
        "LinDi", "CaoDi", "QiTaGouZhuWu", "JiaoTongSheShi", "Others"
    ]

    myscore = SegScore(10, table)
    myscore.update(gt, pre)
    score = myscore.get_scores()
    print('-'*50)
    myscore.print_score(score)
    print('-'*50)
    # print(metrics.classification_report(gt, pre))
    print('-'*50)
    # print(metrics.cohen_kappa_score(gt, pre))
    print('-'*50)

    # print(metrics.confusion_matrix(gt, pre))
    print('-'*50)
    myscore.print_hist()

    # print('FP = ', hist[0, 1])
    # print('FN = ', hist[1, 0])
    # print('P = ', hist[1, 1] / (hist[1, 1]+hist[0, 1]))
    # print('R = ', hist[1, 1] / (hist[1, 1]+hist[1, 0]))
    # test = np.diag(hist)
    # print(test)


if __name__ == "__main__":
    test()
    pass
