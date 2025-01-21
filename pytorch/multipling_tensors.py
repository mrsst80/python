# multiplying tensors
# rule - inner dimentions must match. inner dimension can be changed with transposing a tensor
# rule - result is a tensor with shape equal to outer dimension
import torch


tensor_A = torch.tensor([[8, 4, 9],
                        [7, 1, 5]])

tensor_B = torch.tensor([[9, 9, 4],
                         [1, 3, 5]])

# multiplying tenosr_A by tensor_B will not work, because their inner shpes are different

print(f"Shapes of both tensors: {tensor_A.shape} @ {tensor_B.shape}")
print(f"Tenosor A {tensor_A}")
print(f"Tensor_B {tensor_B}")
#torch.matmul(tensor_A, tensor_B)
print(f"Shape of tensor_A after transposition (columns becomes rows) {tensor_A.T.shape}")
print(f"Multiply transposed tensor_A by tenosr_B {torch.matmul(tensor_A.T, tensor_B)}")