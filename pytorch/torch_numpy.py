#!/usr/bin/env python3
#
# NumPy is a popular scientific Python numerical computing library.
# Because of this, PyTorch has functionality to interact with it.
# 
# * data in NumPy, want in PyTorch tensor -> `torch.from_numpy(ndarray)`
# * PyTorch tensor -> NumPy -> `torch.Ternsor.numpy()`
# NumPy array to tensor
import torch
import numpy as np

array = np.arange(1.0, 8.0)
tensor = torch.from_numpy(array) # warning when converting from numpy to pytorch, pytorch reflects numpy datatype  float64
print(array)
print(tensor)

# change the value of array , what will this do to `tensor`
array = array + 1 # adding 1 to every value of the array. Don't change value of the tenros
print(tensor)

# Tensor to Numpy
tensor = torch.ones(7)
numpy_tensor = tensor.numpy()
