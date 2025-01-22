#!/usr/bin/env python
#
# Shaping, reshaping , squeezing and unsqueezing tensors
# 
# * Reshaping - reshapes an input tensor to a defined shape
# * View - Return a view of an input tensor of certain shape but keep same memory
#as the original tensor
# * Stacking - combine multiple tensors on top of each other(vstack)
# or side by side (hstack)
# * Squeeze - removes all `1` dimensions from a tensor
# * Unsqueeze - add a `1` dimension to a target tensor
# * Permute - Return a view of the input with dimensions permuted(swapped)
# in a certain way

# Lets create a tensor
import torch
x = torch.arange(1., 10.)
print(x)
print(x.shape)

# Add an exta dimension
x_reshaped = x.reshape(1, 9)
print(x_reshaped)
print(x_reshaped.shape)

# Change the view - view shares same memory as original tensor
z = x.view(1, 9)
print(x)
print(x.shape)

# changing z changes x( because a view of a tensor shares the same memory as original tensor)
z[:, 0] = 5
print(x)
print(z)

# Stack tensors on top of each other
x_stacked = torch.stack([x, x, x, x], dim=0)
print(x_stacked)

# Squeeze a tensor - removes all single dimensions from target tensor
y = torch.zeros(2, 1, 2, 1, 2)
""" print(y.size())
y = torch.squeeze(y)
print(y.size())
y = torch.squeeze(y, 0)
print(y.size())
y = torch.squeeze(y, 1)
print(y.size()) """
x = torch.arange(1., 10.)
x_reshaped = x.reshape(1, 9) # Added one more dimension
print(f"Reshaped tensor : {x_reshaped}")
print(f"Size of thereshaped tensor: {x_reshaped.size()}")
x_squeezed = x_reshaped.squeeze()
print(f"Squeezed tensor: {x_squeezed}")
print(f"Shape of squeezed tensor: {x_squeezed.size()}")

# torch.unsqeed
print(f"Previous target : {x_squeezed}")
print(f"Previous shape: {x_squeezed}")
x_unsqueezed = x_squeezed.unsqueeze(dim=0)
print(f"Unsqeezed tensor: {x_unsqueezed}")
print(f"Unsqueezed tensor shape: {x_unsqueezed.size()}")

# torch.permute - rearranges the dimensions of target tensor in prediffined order
# used with images 
# permute is a view
x_original = torch.rand(size=(224, 224, 3)) # [height, width, colour_channels]
print(x_original)

# Indexing ( selecting data from tensors )
# Indexing with PyTorch is similar to indexing with NymPy
import 