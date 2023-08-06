import torch
import torch.nn as nn
import ADAFMNoiseReducer.models.modules.architecture as arch

# Generator
def define_G(gpu_ids, network_G):
    opt_net = network_G
    which_model = opt_net['which_model_G']

    if which_model == 'adaptive_resnet':
        netG = arch.AdaResNet(in_nc=opt_net['in_nc'], out_nc=opt_net['out_nc'], nf=opt_net['nf'],
                             nb=opt_net['nb'], norm_type=opt_net['norm_type'], act_type='relu',
                             upsample_mode='pixelshuffle', adafm_ksize=opt_net['adafm_ksize'])
    else:
        raise NotImplementedError('Generator model [{:s}] not recognized'.format(which_model))

    if gpu_ids:
        assert torch.cuda.is_available()
        netG = nn.DataParallel(netG)
    return netG