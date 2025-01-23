#!/usr/bin/env python3
# Indexing ( selecting data from tensors )
# Indexing with PyTorch is similar to indexing with NumPy
import torch

x = torch.arange(1, 10).reshape(1, 3, 3)
print(x)
print(x.shape)

# Index on the index above
print(x[0])

# Index on the middle bracket
print(x[0][0])

# Index on the most inner bracket (last dimension)
print(x[0][2][2])

# Get all values of the 0 dimension but only the 1 index value of 1st and 2nd dimension
print(x[:, 1, 1])

# Get index 0 of 0th and 1st dimension and all values of 2nd dimension
print(x[0, 0, :])

print(x[:, :, 2])
