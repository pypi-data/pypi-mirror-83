# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

import torch
import torchvision
import PIL
import math
import numpy as np
import os
import copy
import datetime
from . import array as cc_array
from . import maths as cc_maths
from . import combinations as cc_combinations
from .strings import format_float_to_str as cc_strings_format_float_to_str
# import ccalafiore.array
# import ccalafiore.maths
# import ccalafiore.combinations
# import ccalafiore.strings


class Time:
    def __init__(self, range_raw, level, variate_shift=False, permute_shifts=False):
        self.range = cc_array.Range(range_raw)
        self.level = level

        self.permute_shifts = permute_shifts
        self.variate_shift = variate_shift

        if self.variate_shift:
            self.S = abs(self.range.step)
            if self.S == 1:
                self.variate_shift = False
                if self.permute_shifts:
                    self.permute_shifts = False
                self.shifts = np.asarray([0], dtype='i')

            elif self.permute_shifts:
                self.shifts = np.random.permutation(self.S)
            else:
                self.shifts = np.arange(self.S)
        else:
            self.S = 1
            self.shifts = np.asarray([0], dtype='i')

        self.s = 0
        self.shift = self.shifts[self.s]

    def next_shift(self):
        if self.variate_shift:
            if self.s < self.S - 1:
                self.s += 1
            else:
                self.s = 0
                if self.permute_shifts:
                    self.shifts = np.random.permutation(self.S)
            self.shift = self.shifts[self.s]


class Loader:

    def __init__(
            self, directory_root, level_classes, n_levels_directories=None,
            conditions_directories=None, batch_size=None, n_batches=None,
            shuffle=False, time=None, transforms=None, device=None):

        self.directory_root = directory_root
        self.level_classes = level_classes

        self.time = time

        if n_levels_directories is None:
            self.n_levels_directories = len(conditions_directories)
        elif conditions_directories is None:
            conditions_directories = [None] * self.n_levels_directories  # type: list

        self.L = self.n_levels_directories

        self.shuffle = shuffle

        if transforms is None:
            self.transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
        else:
            self.transforms = transforms

        self.conditions_directories_names = [None] * self.L  # type: list
        self.n_conditions_directories = [None] * self.L  # type: list
        self.conditions_directories = [None] * self.L  # type: list

        directory_root_l = self.directory_root
        for l in range(self.L):
            self.conditions_directories_names[l] = os.listdir(directory_root_l)

            if conditions_directories[l] is None:
                self.n_conditions_directories[l] = len(self.conditions_directories_names[l])
                self.conditions_directories[l] = np.arange(self.n_conditions_directories[l])
            else:
                self.conditions_directories[l] = conditions_directories[l]
                self.n_conditions_directories[l] = len(self.conditions_directories[l])

            directory_root_l = os.path.join(directory_root_l, self.conditions_directories_names[l][0])

        if self.time is not None:
            # if self.time.T is None:
            #     self.time.T = self.n_conditions_directories[self.time.level]
            if self.time.range.stop is None:
                self.time.range.stop = self.n_conditions_directories[self.time.level]
            if self.time.level is None:
                self.time.range.level = self.L - 1

            self.conditions_directories[self.time.level] = (
                self.conditions_directories[self.time.level][self.time.range.to_slice()])
            self.n_conditions_directories[self.time.level] = len(self.conditions_directories[self.time.level])

        self.K = self.n_classes = self.n_conditions_directories[self.level_classes]
        self.n_samples = math.prod(self.n_conditions_directories)

        if batch_size is None:
            if n_batches is None:
                self.batch_size = self.n_samples
                self.n_batches = 1
            else:
                self.n_batches = n_batches
                self.batch_size = cc_maths.rint(self.n_samples / self.n_batches)
        else:
            self.batch_size = batch_size
            self.n_batches = cc_maths.rint(self.n_samples / self.batch_size)

        self.samples_indexes = np.arange(self.n_samples)

        if self.shuffle:
            self.batches_indexes = None
        else:
            self.batches_indexes = np.split(self.samples_indexes, self.n_batches, axis=0)

        if self.time.variate_shift:
            self.combinations_directories_no_shift = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))
            self.combinations_directories = np.copy(self.combinations_directories_no_shift)
            self.combinations_directories[:, self.time.level] += self.time.shift
        else:
            self.combinations_directories_no_shift = None
            self.combinations_directories = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))

        self.labels = torch.tensor(
            self.combinations_directories[slice(0, self.n_samples, 1), self.level_classes],
            dtype=torch.int64, device=device)

        combination_directory_str_0 = [self.conditions_directories_names[v][0] for v in range(self.L)]
        directory_0 = os.path.join(self.directory_root, *combination_directory_str_0)
        image_0 = PIL.Image.open(directory_0)
        tensor_0 = self.transforms(image_0)
        # shape_sample_0 = np.asarray(tensor_0.shape)
        # self.shape_sample = shape_sample_0
        # self.shape_batch = np.empty(self.shape_sample.size + 1, self.shape_sample.dtype)
        # self.shape_batch[0] = self.batch_size
        # self.shape_batch[1:] = self.shape_sample
        # self.tensor_batch = torch.empty(tuple(self.shape_batch), dtype=tensor_0.dtype)
        shape_sample_0 = list(tensor_0.shape)
        self.shape_sample = shape_sample_0
        self.shape_batch = torch.Size(tuple([self.batch_size] + shape_sample_0))
        self.tensor_batch = torch.empty(self.shape_batch, dtype=tensor_0.dtype, device=device)
        self.n_dims_samples = self.shape_sample.__len__()
        self.n_dims_batch = self.n_dims_samples + 1
        self.indexes_batch = np.empty(self.n_dims_batch, dtype=object)
        self.indexes_batch[1:] = slice(0, None, 1)

    def load_batches_e(self):

        if self.shuffle:
            self.batches_indexes = np.split(np.random.permutation(self.samples_indexes), self.n_batches, axis=0)
        for b in range(3):
        # for b in range(self.n_batches):
            labels_b = self.labels[self.batches_indexes[b]]
            # batch_size_eb = batches_indexes_e.shape[0]
            for i in range(self.batch_size):
                combination_directory_ebi = self.combinations_directories[self.batches_indexes[b][i], :]
                combination_directory_str_ebi = [
                    self.conditions_directories_names[l][combination_directory_ebi[l]]
                    for l in range(self.L)]
                directory_ebi = os.path.join(self.directory_root, *combination_directory_str_ebi)
                # array_i_cv2 = cv2.imread(directory_i, cv2.IMREAD_COLOR)
                # array_i = PIL.Image.open(directory_ebi)
                #
                # input_tensor_i = self.transforms(array_i)
                self.indexes_batch[0] = i

                image_ebi = PIL.Image.open(directory_ebi)

                # tensor_ebi = self.transforms(image_ebi)
                # self.tensor_batch[tuple(self.indexes_batch[0])] = tensor_ebi
                self.tensor_batch[tuple(self.indexes_batch)] = self.transforms(image_ebi)

            yield [self.tensor_batch, labels_b]

        if (self.time is not None) and self.time.variate_shift:
            self.time.next_shift()
            self.combinations_directories = np.copy(self.combinations_directories_no_shift)
            self.combinations_directories[:, self.time.level] += self.time.shift


def train_early_stop(model, loader, criterion, optimizer, scheduler, I=50):

    # timer = cc_clock.Timer()
    datetime_start = datetime.datetime.today()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Valuation Loss', 'Valuation Accuracy', 'Best Valuation Accuracy', 'Is Better Accuracy']
    n_columns = len(headers)
    new_line_stats = [None] * n_columns  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    best_acc_str = cc_strings_format_float_to_str(best_acc, n_decimals=n_decimals_for_printing)

    i = 0
    e = 0

    while i < I:

        print('Epoch {} - Unsuccessful Epochs {}'.format(e, i) + '\n' + ('-' * 10))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e
        stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i

        # Each epoch has a training and a validation phase
        # training phase
        model.train()  # Set model to training mode

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['training'].load_batches_e():

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history
            torch.set_grad_enabled(True)
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # backward + optimize
            loss_eb.backward()
            optimizer.step()

            torch.set_grad_enabled(False)

            # statistics
            loss_float_eb = loss_eb.item()
            # noinspection PyTypeChecker
            corrects_eb = torch.sum(preds == labels_eb).item()
            acc_eb = corrects_eb / batch_eb.shape[0]

            loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            acc_str_eb = cc_strings_format_float_to_str(acc_eb, n_decimals=n_decimals_for_printing)

            print('Training. Epoch: {:d}. Batch {:d}. Loss: {:s}. Acc: {:s}.'.format(e, b, loss_str_eb, acc_str_eb))

            running_loss_e += loss_float_eb * batch_eb.shape[0]
            running_corrects_e += corrects_eb

            b += 1

        # scheduler.step()

        loss_e = running_loss_e / loader['training'].n_samples
        acc_e = running_corrects_e / loader['training'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # acc_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        acc_str_e = cc_strings_format_float_to_str(acc_e, n_decimals=n_decimals_for_printing)

        print()
        print('Training. Epoch: {:d}. Loss: {:s}. Acc: {:s}. Best Acc: {:s}.'.format(
            e, loss_str_e, acc_str_e, best_acc_str))

        stats['lines'][e][stats['headers']['Training Loss']] = loss_e
        stats['lines'][e][stats['headers']['Training Accuracy']] = acc_e
        # stats['Training Loss'].append(float(loss_e))
        # stats['Training Accuracy'].append(float(acc_e))


        # validation phase
        model.eval()  # Set model to evaluate mode

        # zero the parameter gradients
        optimizer.zero_grad()

        torch.set_grad_enabled(False)

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation'].load_batches_e():

            # forward
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # statistics
            loss_float_eb = loss_eb.item()
            # noinspection PyTypeChecker
            corrects_eb = torch.sum(preds == labels_eb).item()
            acc_eb = corrects_eb / batch_eb.shape[0]

            loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            acc_str_eb = cc_strings_format_float_to_str(acc_eb, n_decimals=n_decimals_for_printing)

            print('Validation. Epoch: {:d}. Batch {:d}. Loss: {:s}. Acc: {:s}.'.format(e, b, loss_str_eb, acc_str_eb))

            running_loss_e += loss_float_eb * batch_eb.shape[0]
            running_corrects_e += corrects_eb

            b += 1

        loss_e = running_loss_e / loader['validation'].n_samples
        acc_e = running_corrects_e / loader['validation'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # acc_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        acc_str_e = cc_strings_format_float_to_str(acc_e, n_decimals=n_decimals_for_printing)

        print()
        print('Validation. Epoch: {:d}. Loss: {:s}. Acc: {:s}. Best Acc: {:s}.'.format(
            e, loss_str_e, acc_str_e, best_acc_str))

        stats['lines'][e][stats['headers']['Valuation Loss']] = loss_e
        stats['lines'][e][stats['headers']['Valuation Accuracy']] = acc_e
        stats['lines'][e][stats['headers']['Best Valuation Accuracy']] = best_acc
        # stats['Valuation Loss'].append(float(loss_e))
        # stats['Valuation Accuracy'].append(float(acc_e))
        # stats['Best Valuation Accuracy'].append(best_acc)

        if acc_e > best_acc:
            stats['lines'][e][stats['headers']['Is Better Accuracy']] = 1
            # stats['Is Better Accuracy'].append(1)
            i = 0
            best_acc = acc_e
            best_acc_str = cc_strings_format_float_to_str(best_acc, n_decimals=n_decimals_for_printing)
            best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
        else:
            stats['lines'][e][stats['headers']['Is Better Accuracy']] = 0
            # stats['Is Better Accuracy'].append(0)
            i += 1

        e += 1
        print()

    E = e

    datetime_end = datetime.datetime.today()
    time_elapsed = datetime_end - datetime_start

    # all_seconds = timer.get_time()
    all_seconds = time_elapsed.seconds
    seconds = all_seconds % 60
    all_minutes = math.floor(all_seconds / 60)
    minutes = all_minutes % 60
    hours = math.floor(all_minutes / 60)

    print('Training complete in {d:d}d {h:d}h {m:d}m {s:d}s'.format(
        d=time_elapsed.days, h=hours, m=minutes, s=seconds))
    print('Number of Epochs is {E:d}'.format(E=E))
    print('Best Validation Acc: {:s}'.format(best_acc_str))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, stats


def train_early_stop_old(model, loader, criterion, optimizer, scheduler, I=50):

    # timer = cc_clock.Timer()
    datetime_start = datetime.datetime.today()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Valuation Loss', 'Valuation Accuracy', 'Best Valuation Accuracy', 'Is Better Accuracy']
    n_columns = len(headers)
    new_line_stats = [None] * n_columns  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    i = 0
    e = 0

    while i < I:

        print('Epoch {} - Unsuccessful Epochs {}'.format(e, i) + '\n' + ('-' * 10))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e
        stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i

        # Each epoch has a training and a validation phase
        for phase in loader.keys():
            if phase == 'training':
                model.train()  # Set model to training mode
            elif phase == 'validation':
                model.eval()  # Set model to validation mode
            else:
                raise ValueError('Unknown phase')

            running_loss_e = 0.0
            running_corrects_e = 0.0  # type: torch.tensor

            b = 0
            # Iterate over data.
            for batch_eb, labels_eb in loader[phase].load_batches_e():

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in training
                with torch.set_grad_enabled(phase == 'training'):
                    outputs = model(batch_eb)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels_eb)

                    # backward + optimize only if in training phase
                    if phase == 'training':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss_eb = loss.item() * batch_eb.size(0)
                # noinspection PyTypeChecker
                running_corrects_eb = torch.sum(preds == labels_eb)

                loss_eb = running_loss_eb / loader[phase].batch_size
                acc_eb = running_corrects_eb.double() / loader[phase].batch_size
                # epoch_acc = running_corrects.double() / loader[phase].n_samples

                print('{}. Epoch: {:d}. Batch {:d}. Loss: {:s}. Acc: {:s}.'.format(phase, e, b, loss_eb, acc_eb))

                running_loss_e += running_loss_eb
                running_corrects_e += running_corrects_eb

                b += 1

            # if phase == 'training':
            #     scheduler.step()

            loss_e = float(running_loss_e / loader[phase].n_samples)
            acc_e = float(running_corrects_e / loader[phase].n_samples)
            # epoch_acc = running_corrects.double() / loader[phase].n_samples

            print('\n{}. Epoch: {:d}. Loss: {:s}. Acc: {:s}. Best Acc: {:s}.'.format(
                phase, e, loss_e, acc_e, best_acc))

            if phase == 'training':
                stats['lines'][e][stats['headers']['Training Loss']] = loss_e
                stats['lines'][e][stats['headers']['Training Accuracy']] = acc_e
                # stats['Training Loss'].append(float(loss_e))
                # stats['Training Accuracy'].append(float(acc_e))
            elif phase == 'validation':
                stats['lines'][e][stats['headers']['Valuation Loss']] = loss_e
                stats['lines'][e][stats['headers']['Valuation Accuracy']] = acc_e
                stats['lines'][e][stats['headers']['Best Valuation Accuracy']] = best_acc

                # stats['Valuation Loss'].append(float(loss_e))
                # stats['Valuation Accuracy'].append(float(acc_e))
                # stats['Best Valuation Accuracy'].append(best_acc)

                if acc_e > best_acc:
                    stats['lines'][e][stats['headers']['Is Better Accuracy']] = 1

                    # stats['Is Better Accuracy'].append(1)
                    i = 0
                    best_acc = acc_e
                    best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
                else:
                    stats['lines'][e][stats['headers']['Is Better Accuracy']] = 0

                    # stats['Is Better Accuracy'].append(0)
                    i += 1
            else:
                raise ValueError('Unknown phase')

        e += 1
        print()

    E = e

    datetime_end = datetime.datetime.today()
    time_elapsed = datetime_end - datetime_start

    # all_seconds = timer.get_time()
    all_seconds = time_elapsed.seconds
    seconds = all_seconds % 60
    all_minutes = math.floor(all_seconds / 60)
    minutes = all_minutes % 60
    hours = math.floor(all_minutes / 60)

    print('Training complete in {d:d}d {h:d}h {m:d}m {s:d}s'.format(
        d=time_elapsed.days, h=hours, m=minutes, s=seconds))
    print('Number of Epochs is {E:d}'.format(E=E))
    print('Best Validation Acc: {:s}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, stats


def load_resnet(name_model, K=None, pretrained=False, device=None):
    # model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet152', pretrained=True)

    if name_model == 'resnet18':
        model = torchvision.models.resnet18(pretrained=pretrained)
    elif name_model == 'resnet34':
        model = torchvision.models.resnet34(pretrained=pretrained)
    elif name_model == 'resnet50':
        model = torchvision.models.resnet50(pretrained=pretrained)
    elif name_model == 'resnet101':
        model = torchvision.models.resnet101(pretrained=pretrained)
    elif name_model == 'resnet152':
        model = torchvision.models.resnet152(pretrained=pretrained)
    else:
        raise ValueError('name_model')

    if K is not None:
        num_ftrs = model.fc.in_features
        # Here the size of each output sample is set to K.
        model.fc = torch.nn.Linear(num_ftrs, K)

    if device is not None:
        if isinstance(device, str):
            if device != 'cpu':
                model = model.to(torch.device(device))
        elif isinstance(device, torch.device):
            if device.type != 'cpu':
                model = model.to(device)

    return model
