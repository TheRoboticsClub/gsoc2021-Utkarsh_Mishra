# GSoC 2021 Utkarsh A. Mishra

## Information regarding this branch

This branch contains all the works done during the community bonding period.
It contains some deep learning regression models and reinforcement learning algorithm implementations with custom environments.
The RL algorithms are modular and can adapt to environments with vector based observations, pixel based observation or both simultaneously. 

## Structure of the branch

    ├── DL_algorithms
    |   ├── DeepPilot                               # Deep Pilot pytorch implementation
    |   |   ├── utils                               
    |   |   |   ├── deep_pilot_dataset.py           # Torchvision custom dataset
    |   |   |   ├── deeppilot.py                    # CNN for Deep Pilot
    |   |   |   └── processing.py                   # Data collecting, processing and utilities
    |   |   └── train.py                            # training code
    |   |
    |   └── PilotNet                                # Pilot Net pytorch implementation
    |       ├── utils                               
    |       |   ├── pilot_net_dataset.py            # Torchvision custom dataset
    |       |   ├── pilotnet.py                     # CNN for Deep Pilot
    |       |   └── processing.py                   # Data collecting, processing and utilities
    |       └── train.py                            # training code
    |
    ├── RL_algorithms                               
    |   ├── DDPG                                    
    |   |   ├── ddpg.py                             # DDPG pytorch implementation
    |   |   └── ddpg_step.py                        # Single update step of DDPG
    |   ├── DQN                                     
    |   |   ├── dqn.py                              # DQN pytorch implementation
    |   |   └── dqn_step.py                         # Single update step of DQN
    |   ├── PPO                                     
    |   |   ├── ppo.py                              # PPO pytorch implementation
    |   |   └── ppo_step.py                         # Single update step of PPO
    |   ├── models                                  
    |   |   ├── image_policies.py                   # Image encoder + state policies
    |   |   ├── policies.py                         # Standard state vector policies
    |   |   ├── image_values.py                     # Image encoder + state + action value functions
    |   |   └── values.py                           # Standard state + action vector value functions
    |   ├── utils                                   
    |   |   ├── GAE.py                              # Generalized advantage estimation
    |   |   ├── MemoryCollector.py                  # Memory collector with multiple cpu threads
    |   |   ├── replay_memory.py                    # replay memory buffer
    |   |   └── *_utils_.py                         # utility files
    |   ├── sample-env                              
    |   |   └── (Custom Gym Env)                    # Custom Gym environment with mixed pixel observations
    |   |                                           # and vector states
    |   └── main.py                                 # main RL code with modular arguments
    └── docs                                                            
        └── references                              # reference paper PDFs

## Setting up this branch

Best to setup a virtual environment with python 3.6

```
cd ~ && mkdir pyenvs && cd pyenvs
pip install virtualenv
virtualenv gsoc21 --python=python3

cd ~
git clone https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra/ gsoc21code
git checkout community_bonding
source ~/pyenvs/gsoc21/bin/activate
python3 -m pip install -r requirements.txt
```

## References