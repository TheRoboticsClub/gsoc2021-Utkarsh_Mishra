#!/usr/bin/env python

import torch
import torch.nn as nn
from torch.distributions import Normal
from torch.distributions import Categorical

def init_weight(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_normal_(m.weight)
        nn.init.constant_(m.bias, 0.0)

class QPolicy(nn.Module):
    def __init__(self, dim_state, dim_action, dim_hidden=64, activation=nn.LeakyReLU):
        super(QPolicy, self).__init__()

        self.dim_state = dim_state
        self.dim_hidden = dim_hidden
        self.dim_action = dim_action

        self.qvalue = nn.Sequential(nn.Linear(self.dim_state, self.dim_hidden),
                                    activation(),
                                    nn.Linear(self.dim_hidden, self.dim_hidden),
                                    activation(),
                                    nn.Linear(self.dim_hidden, self.dim_action))
        self.apply(init_weight)

    def forward(self, states, **kwargs):
        q_values = self.qvalue(states)
        return q_values

    def get_action(self, states):
        q_values = self.forward(states, )
        max_action = q_values.max(dim=1)[1]
        return max_action

class DDPGPolicy(nn.Module):
    def __init__(
        self,
        dim_state,
        dim_action,
        max_action=None,
        dim_hidden=128,
        activation=nn.LeakyReLU,
    ):
        super(DDPGPolicy, self).__init__()
        
        self.dim_state = dim_state
        self.dim_hidden = dim_hidden
        self.dim_action = dim_action

        self.max_action = max_action
        self.action = nn.Sequential(
            nn.Linear(self.dim_state, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_action),
            nn.Tanh(),
        )
        self.apply(init_weight)

    def forward(self, x):
        action = self.action(x)
        return action * self.max_action

    def get_action_log_prob(self, states):
        action = self.forward(states)
        return action, None


class PPOPolicy(nn.Module):
    def __init__(
        self,
        dim_state,
        dim_action,
        max_action=None,
        dim_hidden=128,
        activation=nn.LeakyReLU,
        log_std_min=-20,
        log_std_max=2,
        log_std=0,
        use_sac=False,
    ):
        super(PPOPolicy, self).__init__()

        self.dim_state = dim_state
        self.dim_hidden = dim_hidden
        self.dim_action = dim_action

        self.max_action = max_action
        self.log_std_min = log_std_min
        self.log_std_max = log_std_max
        self.use_sac = use_sac
        self.common = nn.Sequential(
            nn.Linear(self.dim_state, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_hidden),
            activation(),
        )
        self.policy = nn.Linear(self.dim_hidden, self.dim_action)

        if self.use_sac:
            self.log_std = nn.Linear(self.dim_hidden, self.dim_action)
        else:
            self.log_std = nn.Parameter(
                torch.ones(1, self.dim_action) * log_std, requires_grad=True
            )

        self.apply(init_weight)

    def forward(self, x):
        x = self.common(x)
        mean = self.policy(x)
        if self.use_sac:
            log_std = self.log_std(x)
            log_std = torch.clamp(log_std, self.log_std_min, self.log_std_max)
        else:
            log_std = self.log_std.expand_as(mean)
        std = torch.exp(log_std)
        dist = Normal(mean, std)
        return dist

    def get_log_prob(self, state, action):
        dist = self.forward(state)
        log_prob = dist.log_prob(action)
        return log_prob

    def get_action_log_prob(self, states):
        dist = self.forward(states)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action, log_prob

    def rsample(self, states, eps=1e-6):
        dist = self.forward(states)
        u = dist.rsample()
        log_prob = dist.log_prob(u)
        action = torch.tanh(u)
        log_prob -= torch.log(1.0 - action.pow(2) + eps)
        # log_prob = dist.log_prob(u).sum(dim=-1) - (2*(np.log(2) - u - F.softplus(-2*u))).sum(dim=-1)
        return action * self.max_action, log_prob

    def get_entropy(self, states):
        dist = self.forward(states)
        return dist.entropy().mean()

    def get_kl(self, x):
        assert not self.use_sac, "Expect non SAC algorithm !!!"
        x = self.common(x)
        mean = self.policy(x)
        mean_old = mean.detach()
        log_std = self.log_std.expand_as(mean)
        log_std_old = log_std.detach()
        std = torch.exp(log_std)
        std_old = std.detach()
        kl = (
            -1 / 2
            + log_std
            - log_std_old
            + (std_old.pow(2) + (mean_old - mean).pow(2)) / (2 * std.pow(2))
        )
        return kl.sum(dim=1, keepdim=True)


class DiscretePolicy(nn.Module):
    def __init__(
        self, dim_state, dim_action, dim_hidden=128, activation=nn.LeakyReLU
    ):
        super(DiscretePolicy, self).__init__()

        self.dim_state = dim_state
        self.dim_hidden = dim_hidden
        self.dim_action = dim_action

        self.policy = nn.Sequential(
            nn.Linear(self.dim_state, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_hidden),
            activation(),
            nn.Linear(self.dim_hidden, self.dim_action),
            nn.Softmax(dim=-1),
        )
        self.apply(init_weight)

    def forward(self, x):
        action_probs = self.policy(x)
        dist = Categorical(action_probs)
        return dist

    def get_log_prob(self, state, action):
        dist = self.forward(state)
        log_prob = dist.log_prob(action)
        return log_prob

    def get_action_log_prob(self, states):
        dist = self.forward(states)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action, log_prob

    def get_entropy(self, states):
        dist = self.forward(states)
        return dist.entropy().mean()

    def get_kl(self, x):
        action_probs = self.policy(x)
        action_probs_old = action_probs.detach()
        kl = action_probs_old * (
            torch.log(action_probs_old) - torch.log(action_probs)
        )
        return kl.sum(dim=1, keepdim=True)