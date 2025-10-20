#!/usr/bin/env python3
import torch


# GPU = faster computation on numbers
#
# Putting tensors ( and models ) on the GPU
tensor = torch.tensor([1, 2, 3])
print(tensor , tensor.device)

# Check if GPU ( cuda nvidia) or mps for macbook is available
print(torch.mps.is_available())
print(torch.cuda.is_available())


# Mode tensor on GPU
tensor_on_gpu = tensor.to("mps") # For MAC
print(tensor_on_gpu.device)

# Move tensor back to CPU
# If tensor is on GPU , cant transfor to NumPy
tensor_back_to_cpu = tensor_on_gpu.cpu().numpy()
print(tensor_back_to_cpu)