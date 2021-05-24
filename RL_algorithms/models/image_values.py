#!/usr/bin/env python

import torch
import torch.nn as nn


def init_weight(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_normal_(m.weight)
        nn.init.constant_(m.bias, 0.0)


class QValueImage(nn.Module):
    def __init__(self, 
                dim_image, 
                feature_dim, 
                dim_state, 
                dim_action, 
                dim_hidden=128, 
                activation=nn.LeakyReLU):
        super(QValueImage, self).__init__()

        self.dim_image_c = dim_image[0]
        self.dim_image_h = dim_image[1]
        self.dim_image_w = dim_image[2]
        self.feature_dim = feature_dim
        self.dim_state = dim_state
        self.dim_hidden = dim_hidden
        self.dim_action = dim_action

        self.image_net_fc1 = nn.Conv2d(self.dim_image_c, 32, 6, stride=2, padding=0)
        self.image_net_fc2 = nn.Conv2d(32, 64, 4, stride=2, padding=1)
        self.image_net_fc3 = nn.Linear(64*7*7, 512)
        self.image_net_fc4 = nn.Linear(512, self.feature_dim)
        self.image_net_ln4 = nn.LayerNorm(self.feature_dim)

        self.qvalue = nn.Sequential(nn.Linear(self.feature_dim + self.dim_state + self.dim_action, self.dim_hidden),
                                    activation(),
                                    nn.Linear(self.dim_hidden, self.dim_hidden),
                                    activation(),
                                    nn.Linear(self.dim_hidden, 1))
        self.apply(init_weight)

    def forward(self, images, states, actions):

        features = self.image_net_fc1(images)
        features = torch.relu(features)
        features = self.image_net_fc2(features)
        features = torch.relu(features)
        features = features.reshape(features.size(0), -1)
        features = self.image_net_fc3(features)
        features = self.image_net_fc4(features)
        features = self.image_net_ln4(features)

        states_actions = torch.cat([features, states, actions], dim=-1)
        q_value = self.qvalue(states_actions)

        return q_value


class DDPGValueImage(nn.Module):
    def __init__(self, 
                dim_image, 
                feature_dim, 
                dim_state, 
                dim_action, 
                dim_hidden=128, 
                activation=nn.LeakyReLU):
        super(DDPGValueImage, self).__init__()

        self.dim_image_c = dim_image[0]
        self.dim_image_h = dim_image[1]
        self.dim_image_w = dim_image[2]
        self.feature_dim = feature_dim
        self.dim_state = dim_state
        self.dim_action = dim_action
        self.dim_hidden = dim_hidden

        self.image_net_fc1 = nn.Conv2d(self.dim_image_c, 32, 6, stride=2, padding=0)
        self.image_net_fc2 = nn.Conv2d(32, 64, 4, stride=2, padding=1)
        self.image_net_fc3 = nn.Linear(64*7*7, 512)
        self.image_net_fc4 = nn.Linear(512, self.feature_dim)
        self.image_net_ln4 = nn.LayerNorm(self.feature_dim)

        self.value = nn.Sequential(
            nn.Linear(self.feature_dim + self.dim_state + self.dim_action, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, 1)
        )

        self.value.apply(init_weight)

    def forward(self, images, states, actions):

        features = self.image_net_fc1(images)
        features = torch.relu(features)
        features = self.image_net_fc2(features)
        features = torch.relu(features)
        features = features.reshape(features.size(0), -1)
        features = self.image_net_fc3(features)
        features = self.image_net_fc4(features)
        features = self.image_net_ln4(features)

        state_actions = torch.cat([features, states, actions], dim=1)
        value = self.value(state_actions)
        return value

class PPOValueImage(nn.Module):
    def __init__(self, 
                dim_image, 
                feature_dim, 
                dim_state, 
                dim_hidden=128, 
                activation=nn.ReLU):
        super(PPOValueImage, self).__init__()

        self.dim_image_c = dim_image[0]
        self.dim_image_h = dim_image[1]
        self.dim_image_w = dim_image[2]
        self.feature_dim = feature_dim
        self.dim_state = dim_state
        self.dim_hidden = dim_hidden

        self.image_net_fc1 = nn.Conv2d(self.dim_image_c, 32, 6, stride=2, padding=0)
        self.image_net_fc2 = nn.Conv2d(32, 64, 4, stride=2, padding=1)
        self.image_net_fc3 = nn.Linear(64*7*7, 512)
        self.image_net_fc4 = nn.Linear(512, self.feature_dim)
        self.image_net_ln4 = nn.LayerNorm(self.feature_dim)

        self.value = nn.Sequential(
            nn.Linear(self.feature_dim+self.dim_state, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, 1)
        )

        self.value.apply(init_weight)

    def forward(self, images, states):

        features = self.image_net_fc1(images)
        features = torch.relu(features)
        features = self.image_net_fc2(features)
        features = torch.relu(features)
        features = features.reshape(features.size(0), -1)
        features = self.image_net_fc3(features)
        features = self.image_net_fc4(features)
        features = self.image_net_ln4(features)

        value = self.value(torch.cat([features, states], dim=1))
        return value