# GSoC 2021 Utkarsh A. Mishra

## Information regarding this branch

This branch contains all the works done during the first week period.
It contains the DL pilotNet implementation with stacked image dataset.

Blog Post: [https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-1/](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-1/)

## Structure of the branch

    ├── DL_algorithms
    |   └── PilotNetStacked                         # Pilot Net pytorch implementation
    |       ├── utils                               
    |       |   ├── pilot_net_dataset.py            # Torchvision custom dataset for Stacked Images
    |       |   ├── pilotnet.py                     # CNN for Deep Pilot
    |       |   └── processing.py                   # Data collecting, processing and utilities
    |       └── train.py                            # training code
    |
    └── docs                                                            
        └── references                              # reference paper PDFs

## Setting up this branch

Best to setup a virtual environment with python 3.6

```
cd ~ && mkdir pyenvs && cd pyenvs
python3 -m pip install virtualenv
virtualenv gsoc21 --python=python3

cd ~
git clone https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra/ gsoc21code
git checkout week_1
source ~/pyenvs/gsoc21/bin/activate
python3 -m pip install -r requirements.txt
```

## References

1. Rojas-Perez, L.O., & Martinez-Carranza, J. (2020). DeepPilot: A CNN for Autonomous Drone Racing. Sensors, 20(16), 4524. [https://doi.org/10.3390/s20164524](https://doi.org/10.3390/s20164524)
```
@article{rojas2020deeppilot,
  title={DeepPilot: A CNN for Autonomous Drone Racing},
  author={Rojas-Perez, Leticia Oyuki and Martinez-Carranza, Jose},
  journal={Sensors},
  volume={20},
  number={16},
  pages={4524},
  year={2020},
  publisher={Multidisciplinary Digital Publishing Institute}
}
```

2. Bojarski, Mariusz, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D. Jackel et al. "End to end learning for self-driving cars." arXiv preprint arXiv:1604.07316 (2016). [https://arxiv.org/abs/1604.07316](https://arxiv.org/abs/1604.07316)

```
@article{bojarski2016end,
  title={End to end learning for self-driving cars},
  author={Bojarski, Mariusz and Del Testa, Davide and Dworakowski, Daniel and Firner, Bernhard and Flepp, Beat and Goyal, Prasoon and Jackel, Lawrence D and Monfort, Mathew and Muller, Urs and Zhang, Jiakai and others},
  journal={arXiv preprint arXiv:1604.07316},
  year={2016}
}

@article{bojarski2017explaining,
  title={Explaining how a deep neural network trained with end-to-end learning steers a car},
  author={Bojarski, Mariusz and Yeres, Philip and Choromanska, Anna and Choromanski, Krzysztof and Firner, Bernhard and Jackel, Lawrence and Muller, Urs},
  journal={arXiv preprint arXiv:1704.07911},
  year={2017}
}
```