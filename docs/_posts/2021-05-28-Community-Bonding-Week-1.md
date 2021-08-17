---
title: "Community Bonding: Week 1"
excerpt: "An introduction"

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
- Deep Learning

author: Utkarsh Mishra
pinned: false
---

I am glad that I would be collaborating with the great community of Jderobot. It's a great motivation in working with such a group and sharing their passion for developing intelligent robotics applications.
{: .text-justify}

## Preliminaries

I have already been working on this [Pull request](https://github.com/JdeRobot/BehaviorMetrics/pull/157) [1]. I am going to set up this blog where I can write my progress. This [repository](https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra) [2] is going to have  code and documentation for my project in addition to contributing directly into the primary repository of [Behavior Metrics](https://github.com/JdeRobot/BehaviorMetrics) [3].
{: .text-justify}

I am setting up this blog [template](https://github.com/RoboticsLabURJC/colab-gsoc2020-Diego_Charrez) which I think is appropriate and I am excited to use it for the project. Also, it is well organized and easy to personalize.
{: .text-justify}

## Objectives

- [x] Getting Familiar with the existing code base.
- [x] Recognizing and Documenting potential breaks and redundancies in existing pipeline.
- [x] Literature Review of Pilot-Net and DeepPilot-CNN.
- [x] Reproduce Pilot-Net in PyTorch

## The Current Code Base

The overall contribution of the project will be towards Behavior Metrics and [DL Studio](https://github.com/JdeRobot/DeepLearningStudio) [4]. Behavior Metrics is a generalized framework to test various kinds of Deep Learning(DL) and Reinforcement Learning (RL) "brains". Whereas DL Studio is a new repository which is aimed towards deveoping and storing specific DL brains and get those separated from Behavior Metrics. This will simplify the Behavior Metrics repository structure and will be more clean to work with. The current code structure is a bit unstructured in terms of the DL and RL brains in Behavior Metrics. Critical dependencies and builds on docker container gets messed up after some minor changes. This will be minorly fixed with this issue [5]. Moreover, the current framework is built on Tensorflow-2 Keras.
{: .text-justify}
 
## Literature Review

This is one of the primary objectives of this week. There are two significant papers in the current approaches introducing Pilot-Net [6] for autonomous driving tasks and Deep-Pilot [7] for autonomous drone maneuvers. The below is a review of both these approaches.
{: .text-justify}

### Pilot Net: End-to-End Self Driving

The paper introduces a CNN architecture which learns the entire processing pipeline in order to steer an automobile. The CNN structure in given in the figure below where in they used an augmented image (with shifts and rotations) as input and finds out the planned steering angle. They finally train the overall network based on the ground truth steering angle from the training data. The architecture is expected to generate the steering angle with a single image. They also demonstrated the efficiency of their internal steering state in recognising the road markings and boundaries.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/PilotNetarch.png)

### Deep Pilot: CNN for Autonomous Drone Racing

Autonomous Drone Racing has been an active field of exploration. In this paper, a CNN based approach, DeepPilot is proposed. It takes camera images as input and predicts flight commands as output. These flight commands represent the angular position of the drone’s body frame in the roll and pitch angles, thus producing translation motion in those angles; rotational speed in the yaw angle; and vertical speed referred as altitude h. Values for these 4 flight commands, predicted by DeepPilot, are passed to the drone’s inner controller, thus enabling the drone to navigate autonomously through the gates in the racetrack.
{: .text-justify}

They also propose a temporal approach consisting of creating a mosaic image, with consecutive camera frames, and passing it as input to the DeepPilot. They show that this helps to learn the drone’s motion trend regarding the gate, thus acting as a local memory that leverages the prediction of the flight commands. 
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/DeepPilotarch.jpg)


## Pilot Net Pytorch Implementation

This was an interesting opportunity to implement the first open source version of PilotNet on pytorch. While the original framework predicted only the steering angles, my goal was to make the vehicle follow a line on a cicuit by predicting both the linear and angular velocities. The structure was same as that of the original one except now there are 2 output nodes instead of one.
{: .text-justify}

The official code and documentation README can be found here : \\
[Code Link](https://github.com/JdeRobot/DL-Studio/tree/pilotnet/Formula1-FollowLine/PilotNet)

### Preprocessing

The datasets containing images from two circuits were used. One was a simple circuit which contributed around 12000 images and the other was a difficult circuit with many curves contributing around 5000 images. 80% of the data was used for training purposes and rest were all used for testing.
{: .text-justify}

All the images were preprocessed in two steps:
- Image Size: Cropped to required dimensions and resized to (200, 66, 3), the official pilot net dimensions
- Data Augmentation: Random Brightness (+-2%), Contrast  (+-2%), Gaussian Blur with kernel (5,5), (0.1,2.0) normal distribution were applied
{: .text-justify}



### Training Configuration

Below are the training hyperparameters used:
- Epochs: 100
- Learning rate: 0.001 
- Batch size: 256
- Evaluation: Mean Squared Error
- Observations are not normalized i.e. Linear and Angular velocity bounds are [0.0, 13.0] and [-3.0,3.0] respectively.
{: .text-justify}

### Results

Finally the results were obtained on the more complicated circuit with many curves. The vehicle was able to complete the lap successfully. The final video can be seen below:
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/Wt91LbLdzRU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## References

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/157](https://github.com/JdeRobot/BehaviorMetrics/pull/157) \\
[2] [https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra](https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics](https://github.com/JdeRobot/BehaviorMetrics) \\
[4] [https://github.com/JdeRobot/DeepLearningStudio](https://github.com/JdeRobot/DeepLearningStudio) \\
[5] [https://github.com/JdeRobot/BehaviorMetrics/issues/158](https://github.com/JdeRobot/BehaviorMetrics/issues/158) \\
[6] Bojarski, Mariusz, et al. "End to end learning for self-driving cars." arXiv:1604.07316 (2016).
[https://arxiv.org/abs/1604.07316](https://arxiv.org/abs/1604.07316) \\
[7] Rojas-Perez, L.O., & Martinez-Carranza, J. (2020). DeepPilot: A CNN for Autonomous Drone Racing. Sensors, 20(16), 4524. [https://doi.org/10.3390/s20164524](https://doi.org/10.3390/s20164524)
{: .text-justify}

## Issues and Pull Requests

### Pull Requests Updated

- [https://github.com/JdeRobot/BehaviorMetrics/pull/157](https://github.com/JdeRobot/BehaviorMetrics/pull/157)

### Pull Requests Created

- [https://github.com/JdeRobot/BehaviorMetrics/pull/170](https://github.com/JdeRobot/BehaviorMetrics/pull/170)
- [https://github.com/JdeRobot/DL-Studio/pull/1](https://github.com/JdeRobot/DL-Studio/pull/1)