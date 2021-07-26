---
title: "Coding Period: Week 7"
excerpt: "Horizon experiments!"
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
- PilotNet

author: Utkarsh Mishra
pinned: false
---

This week was more of experimenting and fixing thing in DL-Studio, Behavior Metrics for both Formula 1 and Drone tasks.
{: .text-justify}

## Objectives

- [x] Preliminaries and Explore Issues
- [x] Solve Issues with Pull Requests
- [x] Drone Control analysis

## Preliminaries and Explore Issues

Based on last meeting's discussion with mentors, the following issues were to be addressed:
{: .text-justify}

### Issue 1: Add Full Image and Horizon Experiments

Similar to the expeirments of horizon as performed in last week's blog [1] with horizon = 2, the same experiment was to be repeated with horizons 3, 4 and 5. Further, an additional experiment should be conducted in order to understand the necessity of whether we yield the same result using the complete images as it is instead of cropping them down.
{: .text-justify}

### Issue 2: Remove the circuit based filter for Line detection in drone

Based on the current status of the explicit drone brain [3], the individual color filters for detecting red line in simple and many-curves circuit should be replaced with a generalized line detector and corresponding line width calculator.
{: .text-justify}

### Issue 3: Have a proper method of specifying brain kwargs in config and update documentation

With the current config architecture, it is not flexible to specify extra custom parameters required by user defined brains. This should be resolved with a proper structure of specifying such brain kwargs and documentation should be updated. 

### Issue 4: Add DeepPilot code for preliminary Preparation

As the PilotNet experiments are near end, the DeepPilot preliminary code should be prepared for drone DL brains.
{: .text-justify}

## Solve Issues with Pull Requests

To solve the above issues and add update features, the following updates were made:
{: .text-justify}

### PR 1: Added Horizon and Full Image analysis brains

All images in the training dataset were classified into three cases based on extremity as discussed in the last blog [1]. Now, similar to the horizon = 2 analysis, the same experiment was repaeted with horizon = 3 and still the car was able to complete the Montmelo circuit. However, due to computational limitations, experiments with further horizons were not able to complete within this week.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/fullimg_v1/pilotnet-h3.gif){: .center-image}

Next was the full image analysis where the images are not cropped to the road segments but included everything what the formula1 car senses through the camera. This image was padded with black border in order to maintain the 200:66 aspect ratio for PilotNet model.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/fullimg_v1/fullimg.png)

The PilotNet model trained with this approach was able to complete all the circuits expect Montmelo. Although it was trained on the extreme dataset configuration but the pixels available for learning the relation between curvature and position of red line with the outputs were insufficient.
{: .text-justify}

### PR 1 (combined): Modified Drone Brain Line Width Detection

The drone brain used two separate upper bound filters to detect red color:
- [0,50,200] for line detection in simple circuit
- [110,200,115] for many curves circuit

As the explicit brain is targeted to be a very robust brain solving all the circuits, this effects generalization. So, based on the image mask used by the linear velocity controller segment, the most suitable white patch was detected and assumed as the red line. Subsequently the width was detected and proper z-velocities for height control was commanded.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/drones_v2/generalize_filter.png)

Given the above three images, there are three, one and two white patches visible out of which only one is the red line to follow. This was achieved by considering:
{: .text-justify}

- Distance from the center
- Taking the middle one if 3 patches
- Choosing the narrowest one if 2 patches


### PR 2: Added parameters for specifying brain kwargs and updated documentation

Some parameters for custom brains can be set up directly from the *yml* file below the type of the robot which in this example is *f1*. This format is used to setup paths for trained models and any brain kwargs required by the user.

```yml
BrainPath: 'brains/f1/brain_f1_torchstacked.py'
Type: 'f1'
Parameters:
    Model: 'trained_model_name.checkpoint'
    ImageCrop: True 
    Horizon: 4
    ParamExtra: {Specify value}
```     

### PR 3: Added features for DeepPilot in DL-Studio 

DeepPilot [4] [5] is a CNN based approach which takes camera images as input and predicts flight commands as output. These flight commands represent the angular position of the drone’s body frame in the roll and pitch angles, thus producing translation motion in those angles; rotational speed in the yaw angle; and vertical speed referred as altitude h. Values for these 4 flight commands, predicted by DeepPilot, are passed to the drone’s inner controller, thus enabling the drone to navigate autonomously through the gates in the racetrack. The code is added here [6].
{: .text-justify}

```
── Drone-FollowLine
    |
    |── DeepPilot                               # DeepPilot CNN pytorch implementation
        ├── scripts                             # scripts for running experiments 
        ├── utils                               
        |   ├── pilot_net_dataset.py            # Torchvision custom dataset
        |   ├── pilotnet.py                     # CNN for DeepPilot
        |   ├── transform_helpers.py            # Data Augmentation
        |   └── processing.py                   # Data collecting, processing and utilities
        └── train.py                            # training code
```

## References

[1] [https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-6/](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-6/) \\
[2] [https://www.youtube.com/watch?v=CBT9lvKWanQ](https://www.youtube.com/watch?v=CBT9lvKWanQ) \\
[3] [https://www.youtube.com/watch?v=GZs6OIQ_az0](https://www.youtube.com/watch?v=GZs6OIQ_az0) \\
[4] [https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Community-Bonding-Week-1/](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Community-Bonding-Week-1/) \\
[5] Rojas-Perez, L.O., & Martinez-Carranza, J. (2020). DeepPilot: A CNN for Autonomous Drone Racing. Sensors, 20(16), 4524. [https://doi.org/10.3390/s20164524](https://doi.org/10.3390/s20164524) \\
[6] [https://github.com/JdeRobot/DL-Studio/tree/main/Drone-FollowLine](https://github.com/JdeRobot/DL-Studio/tree/main/Drone-FollowLine)
{: .text-justify}

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/202](https://github.com/JdeRobot/BehaviorMetrics/issues/202) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/issues/203](https://github.com/JdeRobot/BehaviorMetrics/issues/203) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics/issues/204](https://github.com/JdeRobot/BehaviorMetrics/issues/204) \\
[4] [https://github.com/JdeRobot/BehaviorMetrics/issues/206](https://github.com/JdeRobot/BehaviorMetrics/issues/206) \\
[5] [https://github.com/JdeRobot/DL-Studio/issues/13](https://github.com/JdeRobot/DL-Studio/issues/13) \\
[6] [https://github.com/JdeRobot/DL-Studio/issues/14](https://github.com/JdeRobot/DL-Studio/issues/14) \\
[7] [https://github.com/JdeRobot/DL-Studio/issues/15](https://github.com/JdeRobot/DL-Studio/issues/15)
{: .text-justify}

### Pull Requests Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/205](https://github.com/JdeRobot/BehaviorMetrics/pull/205) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/207](https://github.com/JdeRobot/BehaviorMetrics/pull/207) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/16](https://github.com/JdeRobot/DL-Studio/pull/16) \\
[4] [https://github.com/JdeRobot/DL-Studio/pull/17](https://github.com/JdeRobot/DL-Studio/pull/17)
{: .text-justify}


### Pull Requests Closed

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/197](https://github.com/JdeRobot/BehaviorMetrics/pull/197) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/201](https://github.com/JdeRobot/BehaviorMetrics/pull/201) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/12](https://github.com/JdeRobot/DL-Studio/pull/12)
{: .text-justify}