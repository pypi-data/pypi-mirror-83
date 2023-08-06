import torch
import torch.nn as nn


class BaseModel():
    def __init__(self, gpu_ids, finetune_norm, _pretrain_model_G, is_train=False):
        self.device = torch.device('cuda' if gpu_ids is not None else 'cpu')
        self.is_train = is_train
        self._pretrain_model_G = _pretrain_model_G
        self.finetune_norm = finetune_norm
        self.schedulers = []
        self.optimizers = []

    def feed_data(self, data):
        pass

    def optimize_parameters(self):
        pass

    def get_current_visuals(self):
        pass

    def get_current_losses(self):
        pass

    def save(self, label):
        pass

    def load(self):
        pass

    def get_network_description(self, network):
        '''Get the string and total parameters of the network'''
        if isinstance(network, nn.DataParallel):
            network = network.module
        s = str(network)
        n = sum(map(lambda x: x.numel(), network.parameters()))
        return s, n

    def load_network(self, load_path, network, strict=True):
        if isinstance(network, nn.DataParallel):
            network = network.module
        network.load_state_dict(torch.load(load_path), strict=strict)
