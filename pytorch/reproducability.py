#!/usr/bin/env python3
# Reproducibility ( trying to take randomg out of random )
#
#
# How a neural network learns
# `start with random numbers -> tensor operations -> update randomg numbers to try and make
# them better representations of the data -> again > again > again....`
#
# https://pytorch.org/docs/stable/notes/randomness.html
import torch

rand_tensor = torch.rand(3, 3)
print(rand_tensor)

# reduce randomnes in neural networks and pytorch comes the concept of random seed
# random seed - control randomness

rand_tensor = torch.rand(3, 3)

# Lets make some random but reproducible tensor
RANDOM_SEED = 5

torch.manual_seed(RANDOM_SEED)  # works for one tensor, needs to be set every type before defining tensor
random_tensor_C = torch.rand(3, 4)

torch.manual_seed(RANDOM_SEED) 
random_tensor_D = torch.rand(3, 4)

print(random_tensor_C)
print(random_tensor_D)
print(random_tensor_C == random_tensor_D)