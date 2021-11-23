import time
import torch
import numpy as np
from argparse import ArgumentParser
from networks.network import LLL_Net
from datasets.auxiliary import aux_loaders
from datasets.memory_dataset import MemoryDataset

from loggers.exp_logger import ExperimentLogger
from datasets.exemplars_dataset import ExemplarsDataset


class Appr:
    """Basic class for implementing incremental learning approaches"""

    def __init__(self, model_cls, device, nepochs=100, lr=0.05, lr_min=1e-4, lr_factor=3, lr_patience=5, clipgrad=10000,
                 momentum=0, wd=0, logger: ExperimentLogger = None, exemplars_dataset: ExemplarsDataset = None):
        self.model_cls = model_cls
        self.model = None
        self.models = []
        self.device = device
        self.nepochs = nepochs
        self.lr = lr
        self.lr_min = lr_min
        self.lr_factor = lr_factor
        self.lr_patience = lr_patience
        self.clipgrad = clipgrad
        self.momentum = momentum
        self.wd = wd
        self.logger = logger
        self.exemplars_dataset = exemplars_dataset
        self.optimizer = None
        self.aux_frac = 1.
        self.aux_type = 'ti'

        self.task_cls = []
        self.task_offset = None

    @staticmethod
    def extra_parser(args):
        """Returns a parser containing the approach specific parameters"""
        parser = ArgumentParser()
        return parser.parse_known_args(args)

    @staticmethod
    def exemplars_dataset_class():
        return ExemplarsDataset

    def _get_optimizer(self):
        """Returns the optimizer"""
        return torch.optim.SGD(self.model.parameters(), lr=self.lr, weight_decay=self.wd, momentum=self.momentum)

    def get_aux_loader(self, trn_loader):

        task_size = int(self.aux_frac * len(trn_loader.dataset))
        task_x = trn_loader.dataset.images
        task_y = trn_loader.dataset.labels
        aux_data = {}

        if isinstance(self.aux_type, str):
            negative_fn = aux_loaders[self.aux_type]
            aux_data['x'] = list(negative_fn(data=task_x,
                                        targets=task_y,
                                        n_samples=task_size))
        elif isinstance(self.aux_type, list):
            aux_data['x'] = []
            task_subsize = task_size // len(self.aux_type)
            for sub_kind in self.aux_type:
                negative_fn = aux_loaders[sub_kind]
                aux_data['x'] += list(negative_fn(data=task_x,
                                                  targets=task_y,
                                                  n_samples=task_subsize))

        aux_data['y'] = task_size * [-1]
        aux_dataset = MemoryDataset(aux_data, transform=trn_loader.dataset.transform)

        neg_loader = torch.utils.data.DataLoader(trn_loader.dataset + aux_dataset,
                                                 batch_size=trn_loader.batch_size,
                                                 shuffle=True,
                                                 num_workers=trn_loader.num_workers,
                                                 pin_memory=trn_loader.pin_memory)

        return neg_loader

    def train(self, t, trn_loader, val_loader):
        """Main train structure"""
        self.pre_train_process(t, trn_loader)
        self.train_loop(t, trn_loader, val_loader)
        self.post_train_process(t, trn_loader)

    def pre_train_process(self, t, trn_loader):
        """Runs before training all epochs of the task (before the train session)"""

        # initialize model for this task
        assert len(self.models) == t, "Stored more models than tasks"

        init_model = self.model_cls(pretrained=False)
        new_model = LLL_Net(init_model, remove_existing_head=True)
        new_model.add_head(2)
        new_model.to(self.device)

        self.task_cls.append(2)
        self.task_offset = torch.cat([torch.LongTensor(1).zero_(), torch.tensor(self.task_cls).cumsum(0)[:-1]])

        self.models.append(new_model)
        self.model = self.models[-1]

    def train_loop(self, t, trn_loader, val_loader):
        """Contains the epochs loop"""
        lr = self.lr
        best_loss = np.inf
        patience = self.lr_patience
        best_model = self.model.get_copy()

        self.optimizer = self._get_optimizer()

        # Loop epochs
        for e in range(self.nepochs):
            # Train
            clock0 = time.time()
            self.train_epoch(t, trn_loader)
            clock1 = time.time()
            print('| Epoch {:3d}, time={:5.1f}s | Train: skip eval |'.format(e + 1, clock1 - clock0), end='')

            # Valid
            clock3 = time.time()
            valid_loss, valid_acc, _ = self.eval(t, val_loader)
            clock4 = time.time()
            print(' Valid: time={:5.1f}s loss={:.3f}, TAw acc={:5.1f}% |'.format(
                clock4 - clock3, valid_loss, 100 * valid_acc), end='')
            self.logger.log_scalar(task=t, iter=e + 1, name="loss", value=valid_loss, group="valid")
            self.logger.log_scalar(task=t, iter=e + 1, name="acc", value=100 * valid_acc, group="valid")

            # Adapt learning rate - patience scheme - early stopping regularization
            if valid_loss < best_loss:
                # if the loss goes down, keep it as the best model and end line with a star ( * )
                best_loss = valid_loss
                best_model = self.model.get_copy()
                patience = self.lr_patience
                print(' *', end='')
            else:
                # if the loss does not go down, decrease patience
                patience -= 1
                if patience <= 0:
                    # if it runs out of patience, reduce the learning rate
                    lr /= self.lr_factor
                    print(' lr={:.1e}'.format(lr), end='')
                    if lr < self.lr_min:
                        # if the lr decreases below minimum, stop the training session
                        print()
                        break
                    # reset patience and recover best model so far to continue training
                    patience = self.lr_patience
                    self.optimizer.param_groups[0]['lr'] = lr
                    self.model.set_state_dict(best_model)
            self.logger.log_scalar(task=t, iter=e + 1, name="patience", value=patience, group="train")
            self.logger.log_scalar(task=t, iter=e + 1, name="lr", value=lr, group="train")
            print()
        self.model.set_state_dict(best_model)

    def post_train_process(self, t, trn_loader):
        """Runs after training all the epochs of the task (after the train session)"""

        self.models[-1].freeze_all()

    def train_epoch(self, t, trn_loader):
        """Runs a single epoch"""

        trn_loader = self.get_aux_loader(trn_loader)

        self.model.train()
        for images, targets in trn_loader:
            # Forward current model
            outputs = self.model(images.to(self.device))
            loss = self.criterion(t, outputs, targets.to(self.device))
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clipgrad)
            self.optimizer.step()

    def eval(self, t, val_loader):
        """Contains the evaluation code"""
        with torch.no_grad():
            total_loss, total_acc_taw, total_acc_tag, total_num = 0, 0, 0, 0
            for images, targets in val_loader:
                # Forward current model
                outputs = []
                for model in self.models:
                    model.eval()
                    outputs.append(model(images.to(self.device))[0])
                loss = self.criterion(t, outputs, targets.to(self.device), eval=True)
                hits_taw, hits_tag = self.calculate_metrics(outputs, targets)
                # Log
                total_loss += loss.item() * len(targets)
                total_acc_taw += hits_taw.sum().item()
                total_acc_tag += hits_tag.sum().item()
                total_num += len(targets)
        return total_loss / total_num, total_acc_taw / total_num, total_acc_tag / total_num

    def calculate_metrics(self, outputs, targets):
        """Contains the main Task-Aware and Task-Agnostic metrics"""
        pred = torch.zeros_like(targets.to(self.device))
        # Task-Aware Multi-Head
        for m in range(len(pred)):
            this_task = (torch.tensor(self.task_cls).cumsum(0) <= targets[m]).sum()
            pred[m] = outputs[this_task][m].argmax() + self.task_offset[this_task]
        hits_taw = (pred == targets.to(self.device)).float()
        # Task-Agnostic Multi-Head
        pred = torch.cat(outputs, dim=1).argmax(1)
        hits_tag = (pred == targets.to(self.device)).float()
        return hits_taw, hits_tag

    def criterion(self, t, outputs, targets, eval=False):
        """Returns the loss value"""

        n_network_outputs = self.model.heads[-1].out_features

        if any(targets < 0):
            neg_ids = torch.where(targets < 0)[0]

            targets = targets - self.task_offset[t]

            targets[neg_ids] = 0
            # one-hot encode target for binary loss
            one_hot_target = torch.nn.functional.one_hot(targets, num_classes=n_network_outputs).float()
            one_hot_target[neg_ids] = torch.zeros(one_hot_target.shape[1]).to(self.device).float()
        else:
            targets = targets - self.task_offset[t]
            one_hot_target = torch.nn.functional.one_hot(targets, num_classes=n_network_outputs).float()

        if eval:
            return torch.nn.functional.binary_cross_entropy_with_logits(outputs[t], one_hot_target)
        else:
            return torch.nn.functional.binary_cross_entropy_with_logits(outputs[0], one_hot_target)


