import cv2 as cv
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.utils.data as data
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision as tv
import logging
import time
import os
import sys
import numpy as np
import random
from PIL import Image

# the program will try to guess the emotion of a person based on a picture of his face
# the framework will be pytorch
# the ai will be a convolutional neural network
# the ai will be trained using reinforcement learning
# the ai will be evaluated by a human and given a reward based on how well it guessed the emotion
# a picture of a face will be taken with cv2 and the emotion of the person will be guessed by the ai
# then the person will evaluate the guess and give a reward to the ai
# the ai will then be trained using the reward

# the ai will be a class with the following methods:
# __init__(): initializes the ai
# guess(): guesses the emotion of a person based on a picture of his face
# evaluate(): evaluates the guess of the ai and gives a reward
# train(): trains the ai using reinforcement learning
# save(): saves the ai to a file
# load(): loads the ai from a file

# the ai will be a convolutional neural network with 5 layers
# the input layer will have 48x48x3 neurons
# the first hidden layer will have 128 neurons
# the second hidden layer will have 64 neurons
# the third hidden layer will have 32 neurons
# the fourth hidden layer will have 16 neurons
# the output layer will have 7 neurons
# the activation function will be relu
# the optimizer will be adam
# the loss function will be mse
# the ai will be trained using reinforcement learning

# ai class
class ai(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conv1 = tv.models.resnet18(pretrained=True)
        self.conv1.fc = nn.Linear(512, 7)
        self.optimizer = optim.Adam(self.parameters())
        self.loss = nn.MSELoss()
        self.reward = 0
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((48, 48)),
            transforms.ToTensor()
        ])
        self.to(torch.device('cuda'))
        self.train()
        
    def guess(self, face: np.ndarray) -> int:
        face = self.transform(face).unsqueeze(0).to(torch.device('cuda'))
        return torch.argmax(self.forward(face)).item()
    
    def evaluate(self, emotion: int) -> None:
        self.reward = 1 if self.emotions[emotion] == input('Is the emotion correct? ') else -1
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv1(x)    
    
    def train(self) -> None:
        self.optimizer.zero_grad()
        self.loss(self.forward(self.transform(Image.open('face.jpg').convert('RGB')).unsqueeze(0).to(torch.device('cuda'))), self.reward).backward()
        self.optimizer.step()
        
    def save(self) -> None:
        torch.save(self.state_dict(), 'ai.pth')
        
    def load(self) -> None:
        self.load_state_dict(torch.load('ai.pth'))
        
# main function
def main() -> None:
    torch.cuda.set_device(0)
    cv.imwrite('face.jpg', cv.VideoCapture(0).read()[1])
    
    ai1 = ai()
    i = 0
    while True:
        cv.imwrite('face.jpg', cv.VideoCapture(0).read()[1])
        ai1.evaluate(ai1.guess(Image.open('face.jpg').convert('RGB'))
        ai1.train()
        ai1.save()
        
        if input('Do you want to continue? ') == 'no' & i >= 100:
            break
        
        i += 1

if __name__ == '__main__':
    main()
