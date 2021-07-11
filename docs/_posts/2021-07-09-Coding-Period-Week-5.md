---
title: "Coding Period: Week 5"
excerpt: "High Variance and Watching Drone struggle!"
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

This week was all about trying to adapt the brains to the variance and modifying drone explicit brain with variable height control in Behavior Metrics.
{: .text-justify}

## Objectives

- [x] Preliminaries and Explore Issues
- [x] Solve Issues with Pull Requests
- [x] Modify the Adaptive Drone Height Control

## Preliminaries and Explore Issues

Based on this week's objective dicussion with my mentors, we concluded that the expliict brain commanded velocities should be compared with our predicted velocities, specifically in the Montmelo setting. As the Z-turn in montmelo is the hardest one, multiple directions are possible.
{: .text-justify}

### Issue 1: High Variance in Training Data

The first issue with the high variance in the dataset is a crucial one as this directly helps in improving the DL-Studio PilotNet framework. There are several possible directions:
{: .text-justify}
- While training, more emphasis should be given to images with high desired angular velocity
- Probabilistic networks with mean and variance can be trained

This time, we go with the first one.

### Issue 2: No independent IMU height control, complete visual control for Drones

With the current formulation of the height control of a drone as an independent PD control operating on the IMu height data, the framework cannnot be intutively used to prepare image based dataset. As all the commands should be a function of only the frontal image, a methodology to represent height control from the image must be implemented.
{: .text-justify}

## Solve Issues with Pull Requests

To solve the above issues and add update features, the following updates were made:
{: .text-justify}

### (Not yet) PR: Increase adaptiveness to high variance

After addressing the variance issue and modifying the dataset as decided, both the base PilotNet brain and PilotNet Stacked brain was retrained and the brains were tested on the unseen montmelo dataset. The comparison of the outputs of the explicit and pilotnet brains are given in the figure below. 
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/analysis_v2/variance.png)

This should be noted that the extreme bang-bang commands of the  explicit controller makes it too difficult for the DL brains to learn and generalize. A future direction can be training probabilistic DL brains which will also consider an uncertainty in the predicted velocity commands.
{: .text-justify}

### (Updated) PR: Implemented complete visual control for drone framework 

Based on the last week's blog video of the explicit brain control of the drone, this week's task modifies the height control with visual inputs i.e. with only the frontal images. When PX4-MAVROS is initialized, it makes the brain takeoff to a very high height. So, for the starting position, no forward speed and rotation commands are given until the drone descends to a desired height of $$1 \pm 0.2$$ meters. Once the drone reaches the desired height, the IMU based height control is disabled and image based control is initiated as shown in the gif below.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/drones_v1/takeoff-explicit.gif){: .center-image}

This time, instead of a target height, a target visual red line width is chosen in order to take the complete advantage of the image. Only the frontal image is used. After cropping the image to only consider it's bottom, a mask was obtained in order to recognize the red line as shown below. 
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/drones_v1/height_masks.png)

The width of the redline as a percentage of the width of the image is considered as the decision variable for PD control. The target red line percentage was taken to be 4% as obtained by analysing the previous IMU based height control. If the observed width is more, the drone should rise up and vice-versa. However, with the height degree of freedom, we also get the pitch degree of freedom in drones. This is typically a challenge because the pitch changes the orientation of the camera and drone perceives different line width at the same height. Thus creating an instability in the system. Future work can be having the target line width as a function of the the pitch of the drone. The obtained behavior is shown in the video below.
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/SmYmEarsaX0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/196](https://github.com/JdeRobot/BehaviorMetrics/issues/196) \\
[2] Updated: [https://github.com/JdeRobot/BehaviorMetrics/issues/192](https://github.com/JdeRobot/BehaviorMetrics/issues/192) \\
[3] [https://github.com/JdeRobot/drones/issues/132](https://github.com/JdeRobot/drones/issues/132)
{: .text-justify}

### Pull Requests Created

[1] Updated: [https://github.com/JdeRobot/BehaviorMetrics/pull/193](https://github.com/JdeRobot/BehaviorMetrics/pull/193) \\
[2] [https://github.com/JdeRobot/drones/pull/134](https://github.com/JdeRobot/drones/pull/134)
{: .text-justify}

### Pull Requests Closed

[1] [https://github.com/JdeRobot/drones/pull/134](https://github.com/JdeRobot/drones/pull/134)
{: .text-justify}