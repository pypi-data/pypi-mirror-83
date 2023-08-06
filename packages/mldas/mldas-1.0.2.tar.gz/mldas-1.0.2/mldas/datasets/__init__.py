__copyright__ = """
Machine Learning for Distributed Acoustic Sensing data (MLDAS)
Copyright (c) 2020, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.
"""
__license__ = "Modified BSD license (see LICENSE.txt)"
__maintainer__ = "Vincent Dumont"
__email__ = "vincentdumont11@gmail.com"

import torchvision, torch, os
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from .dataset import BaseDataset
from .util import load_label

def get_data_loaders(output_dir, batch_size, from_dict, distributed=False,
                     use_dist_sampler_train=True,
                     use_dist_sampler_valid=False,
                     **dataset_args):
    
    # Get the datasets
    if from_dict:
        train_dataset, valid_dataset, test_dataset = get_multilabel(output_dir)
    else:
        train_dataset, valid_dataset, test_dataset = get_datasets(**dataset_args)

    # Distributed samplers
    train_sampler, valid_sampler, test_sampler = None, None, None
    if distributed and use_dist_sampler_train:
        train_sampler = DistributedSampler(train_dataset)
    if distributed and use_dist_sampler_valid and valid_dataset is not None:
        valid_sampler = DistributedSampler(valid_dataset)
    if distributed and use_dist_sampler_valid and test_dataset is not None:
        test_sampler = DistributedSampler(test_dataset)
        
    # Data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size,
                              sampler=train_sampler,
                              shuffle=(train_sampler is None))
    valid_loader = (DataLoader(valid_dataset, batch_size=batch_size,
                               sampler=valid_sampler)
                    if valid_dataset is not None else None)
    test_loader = (DataLoader(test_dataset, batch_size=batch_size,
                               sampler=test_sampler)
                    if test_dataset is not None else None)

    return train_loader, valid_loader, test_loader

def get_datasets(sample_size, img_size, num_labels, data_path, num_channels):

    data_path = data_path+'set_%ik_%ix%i_class%i'%(sample_size,img_size,img_size,num_labels)
    data_path = os.path.expandvars(data_path)
    transform = [transforms.Grayscale()] if num_channels==1 else []
    transform = transforms.Compose(transform+[transforms.ToTensor()])
    train_dataset = torchvision.datasets.ImageFolder(root=data_path+'/train',transform=transform)
    valid_dataset = torchvision.datasets.ImageFolder(root=data_path+'/validation',transform=transform)
    test_dataset = torchvision.datasets.ImageFolder(root=data_path+'/test',transform=transform)
    return train_dataset, valid_dataset, test_dataset

def get_multilabel(output_dir):
    
    rid2name, id2rid, rid2id = load_label(output_dir + '/label.txt')
    num_classes = [len(item)-2 for item in rid2name]
    train_set = BaseDataset(output_dir, "TrainSet", rid2id)
    val_set = BaseDataset(output_dir, "ValidateSet", rid2id)
    test_set = BaseDataset(output_dir, "TestSet", rid2id)
    return train_set, val_set, test_set
    
