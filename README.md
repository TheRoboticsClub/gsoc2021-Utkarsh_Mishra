## GSoC 2021 Utkarsh A. Mishra

# Information regarding this branch

This branch contains all the works done during the community bonding period.
It contains some deep learning regression models and reinforcement learning algorithm implementations with custom environments.
The RL algorithms are modular and can adapt to environments with vector based observations, pixel based observation or both simultaneously. 

# Structure of the branch

    ├── DL_algorithms
    |   ├── DeepPilot                               # Test files (alternatively `spec` or `tests`)
    |   |   ├── utils                               
    |   |   |   ├── deep_pilot_dataset.py           # Test files (alternatively `spec` or `tests`)
    |   |   |   ├── deeppilot.py                    # Test files (alternatively `spec` or `tests`)
    |   |   |   └── processing.py                   # Test files (alternatively `spec` or `tests`)
    |   |   └── train.py                            # Test files (alternatively `spec` or `tests`)
    |   └── PilotNet                                
    |       ├── utils                               
    |       |   ├── pilot_net_dataset.py            # Test files (alternatively `spec` or `tests`)
    |       |   ├── pilotnet.py                     # Test files (alternatively `spec` or `tests`)
    |       |   └── processing.py                   # Test files (alternatively `spec` or `tests`)
    |       └── train.py                            # Test files (alternatively `spec` or `tests`)
    ├── RL_algorithms                               
    |   ├── DDPG                                    
    |   |   ├── ddpg.py                             # Test files (alternatively `spec` or `tests`)
    |   |   └── ddpg_step.py                        # Test files (alternatively `spec` or `tests`)
    |   ├── DQN                                     
    |   |   ├── dqn.py                              # Test files (alternatively `spec` or `tests`)
    |   |   └── dqn_step.py                         # Test files (alternatively `spec` or `tests`)
    |   ├── PPO                                     
    |   |   ├── ppo.py                              # Test files (alternatively `spec` or `tests`)
    |   |   └── ppo_step.py                         # Test files (alternatively `spec` or `tests`)    
    |   ├── models                                  
    |   |   ├── image_policies.py                   # Test files (alternatively `spec` or `tests`)
    |   |   ├── policies.py                         # Test files (alternatively `spec` or `tests`)
    |   |   ├── image_values.py                     # Test files (alternatively `spec` or `tests`)
    |   |   └── values.py                           # Test files (alternatively `spec` or `tests`)
    |   ├── utils                                   
    |   |   ├── GAE.py                              # Test files (alternatively `spec` or `tests`)
    |   |   ├── MemoryCollector.py                  # Test files (alternatively `spec` or `tests`)
    |   |   ├── replay_memory.py                    # Test files (alternatively `spec` or `tests`)
    |   |   └── *_utils_.py                         # Test files (alternatively `spec` or `tests`)
    |   ├── sample-env                              
    |   |   └── (Custom Gym Env)                    # Test files (alternatively `spec` or `tests`)
    |   └── main.py                                 # Test files (alternatively `spec` or `tests`)
    └── docs                                                            
        └── references                              # Load and stress tests

# Setting up this branch





# References