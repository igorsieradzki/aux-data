import pdb

import torch
from ..incremental_learning import Inc_Learning_Appr
from datasets.auxiliary import aux_loaders
from datasets.memory_dataset import MemoryDataset
from datasets.base_dataset import BaseDataset
from argparse import ArgumentParser


class Aux_Inc_Learning_Appr(Inc_Learning_Appr):
    """Basic class for implementing incremental learning approaches"""

    def __init__(self, model, device, nepochs=100, lr=0.05, lr_min=1e-4, lr_factor=3, lr_patience=5, clipgrad=10000,
                 momentum=0, wd=0, multi_softmax=False, wu_nepochs=0, wu_lr_factor=1, fix_bn=False, eval_on_train=False,
                 logger=None, exemplars_dataset=None, aux_frac=1., aux_type='ti', offline_aux=True, aux_first_only=False):
        super(Aux_Inc_Learning_Appr, self).__init__(model, device, nepochs, lr, lr_min, lr_factor, lr_patience,
                                                    clipgrad, momentum, wd, multi_softmax, wu_nepochs, wu_lr_factor,
                                                    fix_bn, eval_on_train, logger, exemplars_dataset)

        self.aux_frac = aux_frac
        self.aux_type = aux_type
        self.offline_aux = offline_aux
        self.aux_first_only = aux_first_only

        assert self.aux_type in ['ti', 'in']

    @staticmethod
    def extra_parser(args):
        """Returns a parser containing the approach specific parameters"""
        parser = ArgumentParser()
        return parser.parse_known_args(args)

    @staticmethod
    def get_aux_parser():
        """Returns a parser containing the approach specific parameters"""
        parser = ArgumentParser()

        parser.add_argument('--aux-first-only', action='store_true',
                            help="")
        parser.add_argument('--aux-frac', default=1., type=float, required=False,
                            help='Number of aux samples to use as a fraction of the task size (default=%(default)s)')
        parser.add_argument('--aux-type', type=str, default=['ti'], choices=['ti', 'in'],
                            help="")
        parser.add_argument('--offline-aux', action='store_true',
                            help="")
        return parser

    def get_aux_loader(self, trn_loader):

        task_size = int(self.aux_frac * len(trn_loader.dataset))
        task_x = trn_loader.dataset.images
        task_y = trn_loader.dataset.labels
        aux_data = {}

        negative_fn = aux_loaders[self.aux_type]
        aux_data['x'] = list(negative_fn(data=task_x,
                                    targets=task_y,
                                    n_samples=task_size))

        aux_data['y'] = task_size * [-1]

        if self.aux_type == 'ti':
            aux_dataset = MemoryDataset(aux_data, transform=trn_loader.dataset.transform)
        elif self.aux_type == 'in':
            aux_dataset = BaseDataset(aux_data, transform=trn_loader.dataset.transform)
        else:
            raise ValueError(f"Unrecognized `aux_type`: {self.aux_type}")

        aux_loader = torch.utils.data.DataLoader(trn_loader.dataset + aux_dataset,
                                                 batch_size=trn_loader.batch_size,
                                                 shuffle=True,
                                                 num_workers=trn_loader.num_workers,
                                                 pin_memory=trn_loader.pin_memory)

        return aux_loader

    def train_loop(self, t, trn_loader, val_loader):

        if self.offline_aux:
            if t == 0:
                trn_loader = self.get_aux_loader(trn_loader)
            elif not self.aux_first_only:
                trn_loader = self.get_aux_loader(trn_loader)

        super().train_loop(t, trn_loader, val_loader)

    def train_epoch(self, t, trn_loader):
        """Runs a single epoch"""

        if not self.offline_aux:
            if t == 0:
                trn_loader = self.get_aux_loader(trn_loader)
            elif not self.aux_first_only:
                trn_loader = self.get_aux_loader(trn_loader)

        self.model.train()
        if self.fix_bn and t > 0:
            self.model.freeze_bn()
        for images, targets in trn_loader:
            # Forward current model
            outputs = self.model(images.to(self.device))
            loss = self.binary_criterion(t, outputs, targets.to(self.device))
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clipgrad)
            self.optimizer.step()

    def criterion(self, t, outputs, targets):
        if self.model.training:
            raise RuntimeError("Negative samples should use `binary_criterion` instead of softmax one during training.")

        return super().criterion(t, outputs, targets)

    def binary_criterion(self, t, outputs, targets):
        """Returns the loss value"""

        n_network_outputs = self.model.heads[t].out_features

        if any(targets < 0):
            neg_ids = torch.where(targets < 0)[0]

            targets = targets - self.model.task_offset[t]

            targets[neg_ids] = 0
            # one-hot encode target for binary loss
            one_hot_target = torch.nn.functional.one_hot(targets, num_classes=n_network_outputs).float()
            one_hot_target[neg_ids] = torch.zeros(one_hot_target.shape[1]).to(self.device).float()
        else:
            targets = targets - self.model.task_offset[t]
            one_hot_target = torch.nn.functional.one_hot(targets, num_classes=n_network_outputs).float()

        return torch.nn.functional.binary_cross_entropy_with_logits(outputs[t], one_hot_target)
