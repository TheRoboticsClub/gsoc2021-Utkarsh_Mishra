---
title: "Coding Period: Week 8 & 9 and Conclusion"
excerpt: "Concluding my GSoC journey and starting my member collaboration!"
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

The last two weeks was more of experimenting with various approaches of controling F1-car and Iris drone in DL-Studio and Behavior Metrics.
{: .text-justify}

## Objectives

- [x] Stacked PilotNet experiments
- [x] DeepPilot CNN with drones
- [x] Concluding my GSoC journey and starting my member collaboration!

## Stacked PilotNet experiments

The stacked PilotNet setup is interesting because it is aimed towards learning temporal relationships without using a memory based network setup like LSTMs. There are a lot of ways to incorporate the set of frames which I would like to explore:
{: .text-justify}

### Case 1: Spanning wide across the horizon 

In the previous experiments as demonstrated in one of my previous blogs [1] the consecutive set of last H-frames are stacked for a H-step stacking and the PilotNet module acts on the setup. While this works but given the frequency of receiving frames (20 Hz), the last H-steps are somewhat very same. So, this makes so siginificant difference from working with a single frame.
{: .text-justify}

This case aims towards having a wider span of the horizon, which means that instead of taking H-consecutive frames, we can choose H-last frames at an interval of M frames. Now, increasing this M to a lot fails the experiments, however a value of 5 tends to work. After analyzing, it seemed that the even M=5 does not significantly changes the frames.
{: .text-justify}

### Case 2: Considering deviations motivated from explicit brain 

The second case is more motivated by the explicit PD brain which works on the error in deviation of the red-line from the middle of the frame. This was we can decide the frames to be stacked based on difference in the deviations.
{: .text-justify}

## DeepPilot CNN with drones

Finally, with the drone dataset [2] [3] and the DeepPilot implementation in Deep Learning Studio [4], I was able to implement a CNN based controller for the Iris drone. The CNN is trained on the dataset and the controller is implemented as a modified DeepPilot with only outputs as the forward velocity, rotation velocity and vertcal velocity. However, the controller is not yet working and fails to learn the correlation of the z-velocity with the red-line width in the image frame. This is a future work. A pull request was made to the Behavior Metrics repository which allows us to test the trained deeppilot networks.
{: .text-justify}

## Concluding my GSoC2021 journey

Finally, my journey as GSoC2021 student with JdeRobot ends with a lot of experiments and learning. I am very happy with the progress I made and I am looking forward to working with the DL-Studio team as a member of the JdeRobot community. I am thankful to the JdeRobot community for giving me such a chance to work on such an interesting project. I am also fortunate that they believed in me and allowed me to work directly on the main repository. Now, with this work: 
{: .text-justify}

- Behavior Metrics has both PyTorch and TensorFlow implementations of the brains.
- DL-Studio has a new implementation of the PilotNet module which is based on the base PilotNet paper.
- There is an added PilotNet stacked setup ready for use in DL-Studio.
- Finally, I was able to introdice Iris drone into Behavior Metrics and DL-Studio with JdeRobot Drones and DeepPilot implementations.

You can find all my videos for this GSoC project in the playlist [5]. I am looking forward to a very productive collaboration as a member of such a knowledgeable community.
{: .text-justify}

## References

[1] [https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-7/](https://theroboticsclub.github.io/gsoc2021-Utkarsh_Mishra/gsoc/Coding-Period-Week-7/) \\
[2] [https://drive.google.com/file/d/1DBvsaw0I_g2zi6RGxEcYSpiFVgbHxM3H/view?usp=sharing](https://drive.google.com/file/d/1DBvsaw0I_g2zi6RGxEcYSpiFVgbHxM3H/view?usp=sharing) \\
[3] [https://drive.google.com/file/d/13KNnjchnV0C7-xMMgip59gLKxPd52Pzr/view?usp=sharing](https://drive.google.com/file/d/13KNnjchnV0C7-xMMgip59gLKxPd52Pzr/view?usp=sharing) \\
[4] [https://github.com/JdeRobot/DeepLearningStudio/tree/main/Drone-FollowLine](https://github.com/JdeRobot/DeepLearningStudio/tree/main/Drone-FollowLine) \\
[5] [https://youtube.com/playlist?list=PLDvnH871wUkGjLuTfd_BlRvljnVNS90Q0](https://youtube.com/playlist?list=PLDvnH871wUkGjLuTfd_BlRvljnVNS90Q0)
{: .text-justify}

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/210](https://github.com/JdeRobot/BehaviorMetrics/issues/210)
{: .text-justify}

### Pull Requests Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/211](https://github.com/JdeRobot/BehaviorMetrics/pull/211)
{: .text-justify}


### Pull Requests Closed

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/205](https://github.com/JdeRobot/BehaviorMetrics/pull/205) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/207](https://github.com/JdeRobot/BehaviorMetrics/pull/207) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/16](https://github.com/JdeRobot/DL-Studio/pull/16) \\
[4] [https://github.com/JdeRobot/DL-Studio/pull/17](https://github.com/JdeRobot/DL-Studio/pull/17)
{: .text-justify}