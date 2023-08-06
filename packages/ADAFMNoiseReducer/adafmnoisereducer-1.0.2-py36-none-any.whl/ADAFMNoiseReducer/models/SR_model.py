from collections import OrderedDict
import torch
import torch.nn as nn
import ADAFMNoiseReducer.models.networks as networks
from  ADAFMNoiseReducer.models.base_model import BaseModel


class SRModel(BaseModel):
    def __init__(self,gpu_ids, network_G, finetune_norm, _pretrain_model_G):
        super(SRModel, self).__init__(gpu_ids, finetune_norm, _pretrain_model_G)

        # define network and load pretrained models
        self.netG = networks.define_G(gpu_ids, network_G).to(self.device)
        self.load()

    def feed_data(self, data, need_HR=False):
        self.var_L = data.to(self.device)  # LR


    def test(self):
        self.netG.eval()
        with torch.no_grad():
            self.fake_H = self.netG(self.var_L)
        self.netG.train()

    def get_current_visuals(self, need_HR=False):
        out_dict = OrderedDict()
        out_dict['LR'] = self.var_L.detach()[0].float().cpu()
        out_dict['SR'] = self.fake_H.detach()[0].float().cpu()
        return out_dict

    def load(self):
        load_path_G = self._pretrain_model_G
        if load_path_G is not None:
            if self.finetune_norm:
                self.load_network(load_path_G, self.netG, strict=False)
            else:
                self.load_network(load_path_G, self.netG)

    def update(self, new_model_dict):
        if isinstance(self.netG, nn.DataParallel):
            network = self.netG.module
            network.load_state_dict(new_model_dict)
