# -*- coding: utf-8 -*-
import torch
import torch.nn.functional as F


def cross_entropy_loss_bi(input_: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return -torch.mean(target * F.log_softmax(input_, dim=-1) + (1. - target) * F.log_softmax(1. - input_, dim=-1))
