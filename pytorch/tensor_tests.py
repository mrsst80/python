import torch
#import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

tensor1 = torch.arange(start=1, end=50, step=5, device="mps")
print(tensor1)
print(tensor1.dtype)
print(tensor1.shape)
print(tensor1.device)
tensor1 = tensor1.to(device="cpu") # move tensor to another device
print(tensor1.device)

"""
Most common errors during operations with tensors
tensors have different types
tensors have different shape
tensors are on different devices ( cpu or gpu )
"""