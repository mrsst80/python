#!/usr/bin/env python3
#
#
# Example of PyTorch end to end workflow
what_were_covering = {1: "data (prepare and loading)",
                      2: "build model",
                      3: "fitting the model to data(training)",
                      4: "making predictions and evaluting a model (inference)",
                      5: "saving and loading the model",
                      6: "putting it all together"}

print(what_were_covering[1])

import torch
from torch import nn # nn contains all of pytorch's bulding blocks for neural networks
import matplotlib.pyplot as plt


# Check PyTorch version
print(torch.__version__)

# Data (preparing and loading)
'''
# Data can be almost anything .. in machine learning

 * Excel spreadsheet
 * Images of any kind
 * Videos (YouTube)
 * Audio
 * DNA
 * Text

Machine Learning is a game of two parts:
1. Get data into a numerical representation.
2. Build a model to learn patterns in that numerical representation.
  '''

# Show case - linera regression formula
# Use linear regression formula to make a straigh line with known **parameters
# Create known parameters

weight = 0.70
bias = 0.3

# Create 
start = 0
end = 1
step =  0.02
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias
'''
print(X[:10], y[:10], len(X), len(y))
print(type(X))
print(type(y))
'''

#!!! Splitting data into training(60%-80%) and test sets ( validation not always )
# Lets create a training and test set with our data

# Create a traing/test split
traing_split = int(0.8 * len(X))
X_train, y_train = X[:traing_split], y[:traing_split]
X_test, y_test = X[traing_split:], y[traing_split:]

print(len(X_train), len(y_train), len(X_test), len(y_test))

# Visualize our data?
# visualize, visualize, visualize
def plot_prediction(train_data=X_train, 
                    train_labels=y_train, 
                    test_data=X_test, 
                    test_labels=y_test,
                    predictions=None):
    '''
    Plots training data, test data and compares predictions
    '''
    plt.figure(figsize=(10,7))
    # Plot training data in blue
    plt.scatter(train_data, train_labels, c='b', s=4, label="Training data")

    # Plot test data in green
    plt.scatter(test_data, test_labels, c="g", s=4, label="Testing data")

    if predictions is not None:
       # Plot the predictions if they exist
       plt.scatter(test_data, predictions, c="r", s=4, label="Predictions")
    
    # Show the legend
    plt.legend(prop={"size": 14})
    print("Saving png file")
    plt.savefig('v.png')

#plot_prediction()

# First pytorch module - linear regression
# Classes - https://realpython.com/python-classes/

'''
What the module does
* start with random values ( weight & bias )
* Look at training data and adjust the random values to better represent ( or get closer to) 
the ideal values (the weight & bias values we used to )

How does it do so?
Through two main algorithms implemented in pytorch
1. Gradient descent - https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi
2. Backpropagation
'''
from torch import nn

class LinearRegressionModel(nn.Module): # <- almost everything in PyTorch inherits from nn.Module
    def __init__(self):
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1,
                                                requires_grad=True,
                                                dtype=torch.float))
        self.bias = nn.Parameter(torch.randn(1,
                                             requires_grad=True,
                                             dtype=float))
        
    def forward(self, x: torch.Tensor) -> torch.Tensor: # x is the imput data
        return self.weights * x + self.bias # this is the linear regression
        

### PyTorch model building essentials
'''
torch.nn - contains all of the builidings of computational graphs (a neural network can be considered computational graph)
torch.nn.Parameters - what parameters should our model try and learn, often a pyTorch layer from torch.nn will set these for us
torch.nn.Module - The base clase for all neural network modules. if you subclass it , you should overwirte ((def) forward method)
torch.optim - this where the optimizes in PyTorch live, they 
def forward() - All nn.Module subclasses require you to overwrite forward(), this method defines what happens in forward computation
 
'''

## Checking the contents of our PyTorch model
torch.manual_seed(42)

model_0 = LinearRegressionModel()
print(list(model_0.parameters()))
print(model_0.state_dict())

# Making prediction using `torch.inference_mode()`
with torch.inference_mode():
    y_preds = model_0(X_test)
    

print(y_preds)
plot_prediction(predictions=y_preds)

# Training model
'''
Train Model
The whole idea of training is for a model to move from some uknown parameters(these may be random) to some known parameters.
Or in other words from poor representation of the data to a better representation of the data.

One way to measure how poor or how wrong your models predictions are is to use a loss function.
loss functions may also be called cost function or criterion in different areas.
For our case, we are going to refer to it as a loss function


** Loss function: *** 
A function to measure how wrong your model's predictions are from the ideal outputs
lower is better.

***Optimiszer : Takes into account the loss of a model and adjusts the model's parameters. (e.g. weight & bias in our case) to improve the loss function.
    * Insite the optimizer you'll often have to set two paramters:
        * params - the model paramters you'd like to optimize, for example params=model_0.paramters()
        * lr(learning rate) - the learning rate is a hyperparamter that defines how big/small the optimizer changes the paramters which each step(a small lr results in samll changes, a large lr results in large changes)
        
And specifically for PyTorch, we need
* A training loop
* A testing loop


'''
# Check out our model's parameters (a parameter is a value that the model sets itself)
model_0.state_dict()

# Setup a loss function
loss_fn = nn.L1Loss()

# Setup an optimized
optimizer = torch.optim.SGD(params=model_0.parameters(),
                            lr=0.01) # lr = learning rate = posibly the most important hyperparameter


### Building a training loop(and a testing loop) in pytorch
'''
A couple of things we need in a training loop:
0. Loop through the data
1. Forward pass (this involves data moving through our model's forward()) to make prediction on data - also cold forward propagation
2. Calculate the loss ( compare forward pass predictions to ground truth labels)
3. Optimizer zero grad
4. Loss backward - move backwards through the network to calculate the gradients of the parameters of our model with respect to the loss
5. Optimizer step - use the optimizer to adjust our model's parameters to try and improve the loss ( gradient descent )

'''

# An epoch is one loop trhough the data .. ( this is hyperparameter because we've set it ourselves )
epochs = 200

# Track different values
epoch_count = []
loss_values = []
test_loss_values = []

### Training
# 0. Loop through the data
for epoch in range(epochs):
    # Set the model to training mode. Other
    model_0.train() # train mode in PyTorch sets all parameters that all parameters require gradients
    
    # 1. Forward pass
    y_pred = model_0(X_train)
    
    # 2. Calcualate the loss
    loss = loss_fn(y_pred, y_train)
    
    # 3. Optimizer zer grad
    optimizer.zero_grad()
    
    # 4. Perform backpropagation on the loss with respect to the paramters of the model
    loss.backward()
    
    # 5. Step the optimizer ( perform gradiant descent )
    optimizer.step() # by default how the optimizer changes will accumulate through the loop so... we have to zero them above in step 3
     
    ### Testing
    model_0.eval() # turns off gradient tracking    

    with torch.inference_mode(): # turns off gradient tracking & a couple more things behind the scenes
        # 1. Do the forward pass
        test_pred = model_0(X_test)
        
        # 2. Calculate the loss
        test_loss = loss_fn(test_pred, y_test)
    
    if epoch % 10 == 0:
        epoch_count.append(epoch)
        loss_values.append(loss)
        test_loss_values.append(test_loss)
        print(f"Epoch: {epoch} | Loss: {loss} | test loss: {test_loss}")
        
        
    #print(model_0.state_dict())

with torch.inference_mode():
    y_preds_new = model_0(X_test)

plot_prediction(predictions=test_pred)
