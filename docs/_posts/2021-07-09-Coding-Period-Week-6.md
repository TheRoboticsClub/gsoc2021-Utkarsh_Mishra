---
title: "Coding Period: Week 6"
excerpt: "Interesting results!"
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

This week was interesting as I was able to complete all the circuits with the PilotNet base and stacked configurations. Furthermore, the drone explicit brain was enhanced as well.
{: .text-justify}

## Objectives

- [x] Preliminaries and Explore Issues
- [x] Solve Issues with Pull Requests
- [x] Drone Control analysis

## Preliminaries and Explore Issues

Based on last meeting's discussion with mentors, the following issues were to be addressed:
{: .text-justify}

### Issue 1: High Variance in Training Data

More focuss should be given to images with high angular velocity commands and the intensity of focus should be directly proportional to the magnitude of angular velocity. The analysis should be done against the performance of explicit brain on Montmelo circuit as performed in last week's blog [1].
{: .text-justify}

### Issue 2: Smoothen visual control for Drones

Based on the current status of the explicit drone brain [2], the brain's pitch degree of freedom goes unstable and loses the road and the line to follow. The reason for this had to be analysed and the brain's performance should be enhanced for both simple and many curves circuit.
{: .text-justify}

### Issue 3: Enhance PilotNet DL-Studio features and configurations

Current PilotNet structure in DL-Studio [3] should have the added requirements of considering:
{: .text-justify}
- full images instead of cropped ones
- normal set of images instead of augmenting the extreme cases

### Issue 4: Update Behaviro Metrics documentation

Update documentation with instructions for running drone experiments.
{: .text-justify}

## Solve Issues with Pull Requests

To solve the above issues and add update features, the following updates were made:
{: .text-justify}

### PR 1: Increase adaptiveness to high variance with extreme augmentation

All images in the training dataset were classified into three cases based on magnitude of angular velocity targets such that:
{: .text-justify}
- case 1: omega < 1
- case 2: omega > 1
- case 3: omega > 2

The main dataset was augmented with 5 times that of case 2 and 10 times that of case 3. The base PilotNet brain was trained again and the output was again analysed as compared to the explicit brains. A similar operation was done for Stacked PilotNet brain where based on a given horizon, the sequential set of images represented one input to the neural network. The analysis is given below:
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/analysis_v3/comparison.png)

Eventually, both the base and stacked PilotNet brain varaints were able to complete the Montmelo circuit along with all others. An interesting fact is that the stacked brain took less training epochs to complete the Z-cornering. Their performance in shown in the video below. 
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/CBT9lvKWanQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### PR 1 combined: Smoothen visual control for drone framework 

The explicit drone setting as described in my last blog post [1] was suffering from unstability in pitch degree of freedom. The reason for this unstability particularly comes from sudden changes in the linear speed commands as evident from figure below (left). Further, a horizon was added and the moving averag eover this horizon was sent into the drone module as the commanded linear velocity. Finally, after some ablations, a good horizon was chosen to be 100 with minimal pitch disturbances as shown in figure below (right). 
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/drones_v2/horizon.png){: .center-image}

The performance of this change along with minor coeffcient tuning was observed in both simple and many curves circuits. The performance video is shown below.
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/GZs6OIQ_az0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### PR 2 (Incomplete): Added features for PilotNet in DL-Studio 

Some instructions for running drone experiments were added in the documentation.
{: .text-justify}

### PR 3: Added features for PilotNet in DL-Studio 

The following features were added for pre-processing and checkpoint restoration.
{: .text-justify}
- Cropped-NoCropped preprocessing of images while reading them from the dataset folders.
- Implementing the extreme cases as described [above](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-6/#pr-1-increase-adaptiveness-to-high-variance-with-extreme-augmentation) for dataset augmentation
- Safe checkpoint saving and restoration from the same epoch and training conditions.
- Adding the best performaning experiment results for reference and updating usage documentation [3].

## References

[1] [https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-5/](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-5/) \\
[2] [https://www.youtube.com/watch?v=SmYmEarsaX0](https://www.youtube.com/watch?v=SmYmEarsaX0) \\
[3] [https://github.com/JdeRobot/DL-Studio/tree/main/Formula1-FollowLine](https://github.com/JdeRobot/DL-Studio/tree/main/Formula1-FollowLine)  
{: .text-justify}

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/198](https://github.com/JdeRobot/BehaviorMetrics/issues/198) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/issues/199](https://github.com/JdeRobot/BehaviorMetrics/issues/199) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics/issues/200](https://github.com/JdeRobot/BehaviorMetrics/issues/200) \\
[4] [https://github.com/JdeRobot/DL-Studio/issues/11](https://github.com/JdeRobot/DL-Studio/issues/11)
{: .text-justify}

### Pull Requests Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/197](https://github.com/JdeRobot/BehaviorMetrics/pull/197) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/201](https://github.com/JdeRobot/BehaviorMetrics/pull/201) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/12](https://github.com/JdeRobot/DL-Studio/pull/12)
{: .text-justify}


### Pull Requests Closed

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/193](https://github.com/JdeRobot/BehaviorMetrics/pull/193)
{: .text-justify}