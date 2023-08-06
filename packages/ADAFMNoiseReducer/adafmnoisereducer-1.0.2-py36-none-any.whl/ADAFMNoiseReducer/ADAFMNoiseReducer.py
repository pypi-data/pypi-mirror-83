import torch
import os
import numpy as np
from collections import OrderedDict
from ADAFMNoiseReducer.models.SR_model import SRModel
from ADAFMNoiseReducer.utils import tensor2img

class ADAFMNoiseReducer:
    def __init__(self, coef=0.6, gpu_ids=[0], stride=0.1):
        self._model = "sr"
        self._gpu_ids = gpu_ids
        self.coef = coef
        self.stride = stride
        self._interpolate_stride = stride
        self._pretrain_model_G = os.path.join(os.path.dirname(__file__), "ADAFMNoiseReducerModel.pth")
        self._network_G = {
            "which_model_G": "adaptive_resnet"
            , "norm_type": "adafm"
            , "nf": 64
            , "nb": 16
            , "in_nc": 3
            , "out_nc": 3
            , "adafm_ksize": 1
            }

        # Create model
        self.model = SRModel(self._gpu_ids, self._network_G, None, self._pretrain_model_G)
        self.model_dict = torch.load(self._pretrain_model_G)

        # Update the model
        print('setting coef to {:.2f}'.format(self.coef))
        interp_dict = self.model_dict.copy()
        for k, v in self.model_dict.items():
            if k.find('transformer') >= 0:
                interp_dict[k] = v * self.coef
        self.model.update(interp_dict)

    def convert(self, img_LR):
        """

        """
        img_LR = img_LR.astype(np.float32) / 255.
        if img_LR.ndim == 2:
            img_LR = np.expand_dims(img_LR, axis=2)
        if img_LR.shape[2] > 3:
            img_LR = img_LR[:, :, :3]
        if img_LR.shape[2] == 3:
            img_LR = img_LR[:, :, [2, 1, 0]]
        img_LR = np.ascontiguousarray(np.transpose(img_LR, (2, 0, 1)))
        img_LR = img_LR.reshape((1,) + img_LR.shape)
        img_LR = torch.from_numpy(img_LR).float()
        return img_LR

    def __call__(self, img):
        data = self.convert(img)
        self.model.feed_data(data)
        self.model.test()
        visuals = self.model.get_current_visuals()
        sr_img = tensor2img(visuals['SR'])
        return sr_img

