---
title: "Summary and Recap"
excerpt: "Easy interpretation for the interested ones!"
usemathjax: true
sidebar:
  nav: "docs"

toc: true
toc_label: "Contents"
toc_icon: "cog"


categories:
- GSoC
tags:
- Jderobot
- Behavior Metrics
- DL Studio
- DeepPilot

author: Utkarsh Mishra
pinned: false
---

This has been a great journey and so far. Below you will find a concise summary of my contribution to the JdeRobot community as a Google Summer of Code student.
{: .text-justify}

## Objectives

- [x] PyTorch Extension
- [x] Randomization and Visualization
- [x] DeepLearningStudio: PilotNet base and stacked setups
- [x] Iris drone into Behavior Metrics
- [x] DeepPilot CNN for Drone Neural control

## PyTorch Extension to Behavior Metrics

Before GSoC 2021, Behavior Metrics used to support Tensorflow based brains. My contributions included implementing and extending all the necessary components to support PyTorch based brains. This started from the community bonding period and I was able to implement both the Deep Learning and Reinforcement learning algorithms. You can refer to the following:
{: .text-justify}
- [Preliminary Code](https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra/tree/community_bonding)
- [Blog Post 1](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Community-Bonding-Week-1/)
- [Blog Post 2](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Community-Bonding-Week-2/)


## Randomization and Visualization in Behavior Metrics

Randomization for various initial positions in script mode was extended to GUI method and the same was done for the visualization of the behavior metrics. This was done by implementing the randomization module separately and extending the existing code to better remote saving of visualized performance plots. Further, the information and custom hyperparameter flow from config files to respective brains was origanized and structured.   You can refer to the following:
{: .text-justify}
- [Behavior Metrics PR #182, #183, #184, #185](https://github.com/JdeRobot/BehaviorMetrics)
- [Blog Post 1](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-2/)
- [Blog Post 2](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-4/)

## PilotNet base and stacked setups



