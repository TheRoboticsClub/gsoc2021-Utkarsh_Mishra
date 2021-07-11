---
title: "Coding Period: Week 4"
excerpt: "Deep Learning Continues and Drone stuffs!"
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

This week was experimenting with Stacked PilotNet and integrating jderobot_drone with Behavior Metrics.
{: .text-justify}

## Objectives

- [x] Preliminaries and Explore Issues
- [x] Solve Issues with Pull Requests
- [x] Analyze the New Drone integration

## Preliminaries and Explore Issues


{: .text-justify}

With this as the beginning, this week's task was to sort the proper randomization of the initial positions. And then explore the intrdoution of drone into BehaviorMetrics. I found the following directions (as issues):
{: .text-justify}

### Issue 1: Proper Randomization in GUI and Script mode

The issue is observed when we select indexes greater than half for random initialization node from the data bag. An improper randomization causes brains to crash early which is not a good practice. Although, any such evaluation where the brain crashes early is ignored, but such a situation should be avoided.
{: .text-justify}

### Issue 2: Add PilotNet stacked config, trained models and brain

After preparing and training the stacked PilotNet framework in DL-Studio, its time to see how they perform in Behavior Metrics.
{: .text-justify}

### Issue 3: Add Drone explicit brain for line following objective

With MAVROS and PX4 support, it is time to setup Iris drone on the same circuit as the F1 car and make it complete the line following task.
{: .text-justify}

### Issue 4: Add drone assets for BehaviorMetrics drone F1 setup

Once the drone integration is done, the installation of the drone assets should be included in the setup files of Behavior Metrics and proper installation instructions should be given.
{: .text-justify}

## Solve Issues with Pull Requests

To solve the above issues and add update features, the following PRs were created:
{: .text-justify}

### PR 1: Randomization added and only one function for both GUI and SCRIPT mode

Now there is only one function `tmp_random_initializer` in [1] which does all the work of randomization both in GUI and script mode. The function definition is given below. Such a function creates a temporary file derived from the primary circuit world and launch files. 
{: .text-justify}
```python
def tmp_random_initializer(
  current_world,        # Current circuit from config
  stats_perfect_lap,    # Statistics of the perfect lap in that circuit
  randomize=False,      # Randomize initial pose
  gui=False,            # Enable display (in GUI) or background (in Script)
  launch=False          # Launch the tmp files (for script mode)
):
```

### PR 2: Added PilotNet Stacked execution files

The stacked PilotNet brain, config and trained network weights were added and tested on all the circuits. The brain is able to complete all teh circuits except Montmelo at the max speed. However, with a hack, it completes the Montmelo circuit too but with a lesser speed. A video showing the performance of the stacked pilotnet framework in Montmelo circuit is shown below. 
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/pbYfdXvtRLo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

A future line of thought is to modulate the dataset such that the brains get an intuition of when to follow a lesser speed and when to go for maximum speeds. The failure of my trained brains in montmelo circuit is shown in the second half of a previous video [2].
{: .text-justify}

### PR 3: Added explicit brain setup for drone 

This was an interesting task as it introduces drones in the Behavior Metrics framework. The pipeline of drones is a bit different from that of the F1 car. The `DroneWrapper` developed in [3] does most of the work and there are no explicit sensors or actuators which are required. Thus, this difference between the car and drone pipeline had to be taken care of and hence, proper condition statements were introduced in the base Behavior Metrics pipeline. I understood how:
{: .text-justify}
- the setup files are setting up the assets
- px4 mavlink launches the drone
- custom world setups are made

This task was accompanied by replicating a similar explicit brain for drone as developed in [4] for car. The same principle worked except that a height control was added to command the z-velocity based on a PD control law. Below is a video showing the performance of explicit brain with Iris drone and PX4-Mavros backend.
{: .text-justify}

<iframe width="560" height="315" src="https://www.youtube.com/embed/tYxpQDsVI6c" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### PR 4: Added drone assets for BehaviorMetrics

Now, after setting up the custom drone worlds and launch files for all the circuits, the assets should be updated in order to make it avaiable to others. Considering the baseline setup and following the `CustomRobots` [5] structure, a similar structure was formulated and added as a PR to the repository. However, as `JdeRobot/drones` [3] is the primary repository for this setup, the assets will be moved there soon.
{: .text-justify}


## References

[1] [https://github.com/JdeRobot/BehaviorMetrics/blob/noetic-devel/behavior_metrics/utils/random_initializer.py](https://github.com/JdeRobot/BehaviorMetrics/blob/noetic-devel/behavior_metrics/utils/random_initializer.py) \\
[2] [https://youtu.be/u7myt5Ge0ks](https://youtu.be/u7myt5Ge0ks) \\
[3] [https://github.com/JdeRobot/drones/tree/noetic-devel](https://github.com/JdeRobot/drones/tree/noetic-devel) \\
[4] [https://github.com/JdeRobot/BehaviorMetrics/blob/noetic-devel/behavior_metrics/brains/f1/brain_f1_explicit.py](https://github.com/JdeRobot/BehaviorMetrics/blob/noetic-devel/behavior_metrics/brains/f1/brain_f1_explicit.py) \\
[5] [https://github.com/JdeRobot/CustomRobots/tree/noetic-devel](https://github.com/JdeRobot/CustomRobots/tree/noetic-devel) 
{: .text-justify}

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/188](https://github.com/JdeRobot/BehaviorMetrics/issues/188) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/issues/190](https://github.com/JdeRobot/BehaviorMetrics/issues/190) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics/issues/192](https://github.com/JdeRobot/BehaviorMetrics/issues/192) \\
[4] [https://github.com/JdeRobot/CustomRobots/pull/87](https://github.com/JdeRobot/CustomRobots/pull/87)
{: .text-justify}

### Pull Requests Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/189](https://github.com/JdeRobot/BehaviorMetrics/pull/189) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/191](https://github.com/JdeRobot/BehaviorMetrics/pull/191) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics/pull/193](https://github.com/JdeRobot/BehaviorMetrics/pull/193) \\
[3] [https://github.com/JdeRobot/CustomRobots/pull/88](https://github.com/JdeRobot/CustomRobots/pull/88)
{: .text-justify}

### Pull Requests Closed

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/187](https://github.com/JdeRobot/BehaviorMetrics/pull/187) \\
[2] [https://github.com/JdeRobot/DL-Studio/pull/4](https://github.com/JdeRobot/DL-Studio/pull/4) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/5](https://github.com/JdeRobot/DL-Studio/pull/5) \\
[4] [https://github.com/JdeRobot/BehaviorMetrics/pull/189](https://github.com/JdeRobot/BehaviorMetrics/pull/189) \\
[5] [https://github.com/JdeRobot/BehaviorMetrics/pull/191](https://github.com/JdeRobot/BehaviorMetrics/pull/191)
{: .text-justify}