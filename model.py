import torch
import torch.nn as nn

class ChessNeuralNet(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(ChessNeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_sizes[0])
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_sizes[1], output_size)  # Output layer

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


model = ChessNeuralNet(input_size=10, hidden_sizes=[64, 32], output_size=5)
print(model)
