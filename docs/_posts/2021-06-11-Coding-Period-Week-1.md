---
title: "Coding Period: Week 1"
excerpt: "COVID slowed the progress!"
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
- DL Studio
- Deep Learning

author: Utkarsh Mishra
pinned: false
---

This week was all about getting infected by and recovering from Covid-19.
{: .text-justify}

## Objectives

- [x] Stacked PilotNet setup
- [x] Covid Recovery

## Preliminaries about Stacked Dataset

While we collect image data from the circuits and PD controlled explicit brain, the images and their corresponding labels get stored in a sequential manner, basically in the sequence they appear. Also, instantaneous images don't depict the importance of linear velocities. Thus, we need to come up with a strategy wherein the brain should get not only get the current image but also an intuition of the changes in the images relating to the final desired velocities. This is expected to help in tackling various complicated corners in the circuit.
{: .text-justify}

So, the dataset prepared for this task samples a sequence of images upto a specified horizon (which is kept constant for an expeirment) and assigns the label as the the ground truth label of the final sampled image. Although, this is a very basic setup, but it is capable enough of studying if this kind of a setup really helps in undertanding the pattern of change in desired velocities by naively giving the brain intuition of a memeory.
{: .text-justify}

## Setting up Stacked PilotNet

With the above dataset, the same pilotnet brain was used with modified number of channels for each hidden layer. The output of the network was kept the same. This setup kindof resembled the DeepPilot CNN for drones and is a starting point for more complicated LSTM brains.
{: .text-justify}

## Simulation Analysis and Results

No visualizations yet. Although the scripts are ready, will get back to visualizations of the trained brains next week.
{: .text-justify}

## Recovering from Covid-19

Unfortunately, I got infected from Covid-19 virus on 7th of June (coincidently the starting day of the coding period!!) and eventually my whole family was infected. So, this week was less of GSoC and more of fighting Covid-19 together. This impact will definitely take some time to heal but I hope to catch up with my regular progress rate soon.

## References

[1] [https://github.com/JdeRobot/BehaviorMetrics/tree/noetic-devel/gym-gazebo](https://github.com/JdeRobot/BehaviorMetrics/tree/noetic-devel/gym-gazebo) \\
[2] [https://gym.openai.com/](https://gym.openai.com/)