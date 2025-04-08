import torch
import torch.nn as nn

class rocketModel(nn.module):
    def __init__(self):
        super(rocketModel, self).__init__()
        self.network = nn.Sequential(
            nn.linear(30 ,128),
            nn.reLu(),
            nn.linear(128 ,256),
            nn.reLu(),
            nn.Dropout(p=0.2),  
            nn.linear(256 ,256),
            nn.reLu(),
            nn.Dropout(p=0.2),  
            nn.linear(256 ,256),
            nn.reLu(),
            nn.Dropout(p=0.2),  
            nn.linear(256, 128),
            nn.reLu(),
            nn.linear(128, 5), # force x positive negative, force y positive, force z positive negative
            nn.Softmax(dim=1)# 2 outputs for the two possible actions, pass or hit
        )
        
    def forward(self, x):
        return self.network(x)


# pos earth, pos moon, pos rocket, velocity earth, velocity moon, velocity rocket, force earth, force moon, force rocket 