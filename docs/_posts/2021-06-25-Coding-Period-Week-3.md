---
title: "Coding Period: Week 3"
excerpt: "Back to Deep Learning!"
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

Afetr adding all the new features to Behavior Metrics, this week was all about going back to PilotNet implementation and exploring various augmentations.
{: .text-justify}

## Objectives

- [x] Preliminaries and Explore Issues
- [x] Solve Issues with Pull Requests
- [x] Analyze the New Data Augmentations
- [x] Some analysis on Stacked PilotNet

## Preliminaries and Explore Issues


{: .text-justify}

With this as the beginning, this week's task was to sort the data augmentation tools.
I found the following directions (as issues):
{: .text-justify}

### Issue 1 (Unrelated): Update documentation for Behavior Metrics with new features

New features which were added:
- Randomization in GUI mode and choice of randomization in script mode.
- Minor fixes in brains to avoid broken image in loop.
- All image data in Ros bags published as separate image topics.
- Off-Display generation of complete analysis of a brains performance with selected config file.

All these were added to the documentation [1]. 
{: .text-justify}

### Issue (Unrelated): First Image in script mode is broken while in GUI mode works perfect

This is critically a system issue, so I will not be digging up more on this issue. The main reason is the launching time of brain and gazebo, and how the system performs the initialization.
{: .text-justify}

### Issue 2: More Data augmentations to PilotNet framework in DL-studio

Based on previous trainings on the current setup of PilotNet in DL-studio [2], the analysis showed that the trained brain performs quite well in all the circuits and completes them except the Montmelo circuit as shown before in [3]. Hence, the goal is to explore various data augmentations which might help in better generalization.
{: .text-justify}

### Issue 3: Add Stacked PilotNet framework to DL-Studio and preliminary analysis

The PilotNet setup with horizon based dataset consisting of sequentially stacked images as shown before in [4] is to be added to DL-Studio with preliminary analysis.
{: .text-justify}

## Solve Issues with Pull Requests

To solve the above issues and add update features, the following PRs were created:
{: .text-justify}

### PR 1: Updated Documentation for Behavior Metrics

The above requirements of issue 1 were fulfilled and updated. 
{: .text-justify}

### PR 2: Added more data augmentation features 

Various relevant data augmentations were chosen based on the task at hand from the ones provided by TorchVision in [5]. Mostly, minor augmnetations on color was tried as we are not expected to be color invariant. Furthermore, the gaussian blur was given the most importance. It is worth to be noted that the perspective and affine transform might also mislead as the turns might seem more curvy but the target velocity is same. Specifications about the current augmentations:
{: .text-justify}

```python
'gaussian': transforms.GaussianBlur(5, sigma=(0.1, 2.0)),
'jitter': transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
'perspective':transforms.RandomPerspective(distortion_scale=0.3, p=1.0),
'affine':transforms.RandomAffine(degrees=(-10, 10), translate=(0.1, 0.2), scale=(0.9, 1)),
'posterize':transforms.RandomPosterize(bits=2)
```

**PilotNet Case 1: Only Gaussian Augmentation**

The first expeirment was with a simple gaussian augmentation where the image was blurred randomly with a bounded noise. An example of how the images look after transform can be seen in the following figure and the loss curve can be seen further below case 3. The loss curve is quite less for this case as the labels were normalized.
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/augs_v1/case1.png)

**PilotNet Case 2: Gaussian and Perspective Augmentation**

Then the perspective transform was added to slightly modify the perspective as shown below:
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/augs_v1/case2.png)

**PilotNet Case 3: Gaussian, Perspective and Affine Augmentation**

Finally, the affine tranformation was added to further complicate the augmentation strategy, it can be realized from the set of images given below. However, the addition of affine transform on top of perspective transform did not being any change in the learning curve as evident from the training curves further below:
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/augs_v1/case3.png)

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/augs_v1/loss.png)


### PR 3: Added stacked PilotNet experiments


{: .text-justify}

### Stacked PilotNet Case 1: Only Gaussian Augmentation

An example of the percentage completed plots for all the runs in simple_ciruit, many_curves and nurbergring circuits are given in the figure below:
{: .text-justify}

![]({{ site.url }}{{ site.baseurl }}/assets/images/blogs/augs_v1/case3.png)

## References

[1] [https://jderobot.github.io/BehaviorMetrics/quick_start/](https://jderobot.github.io/BehaviorMetrics/quick_start/) \\
[2] [https://github.com/JdeRobot/DL-Studio](https://github.com/JdeRobot/DL-Studio) \\
[3] [https://youtu.be/u7myt5Ge0ks](https://youtu.be/u7myt5Ge0ks) \\
[4] [https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra/tree/week_1/DL_algorithms](https://github.com/TheRoboticsClub/gsoc2021-Utkarsh_Mishra/tree/week_1/DL_algorithms) \\
[5] [https://pytorch.org/vision/stable/transforms.html](https://pytorch.org/vision/stable/transforms.html)
{: .text-justify}

## Issues and Pull Requests

### Issues Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/issues/186](https://github.com/JdeRobot/BehaviorMetrics/issues/186) \\
[2] [https://github.com/JdeRobot/DL-Studio/issues/2](https://github.com/JdeRobot/DL-Studio/issues/2) \\
[3] [https://github.com/JdeRobot/DL-Studio/issues/3](https://github.com/JdeRobot/DL-Studio/issues/3)
{: .text-justify}

### Pull Requests Created

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/187](https://github.com/JdeRobot/BehaviorMetrics/pull/187) \\
[2] [https://github.com/JdeRobot/DL-Studio/pull/4](https://github.com/JdeRobot/DL-Studio/pull/4) \\
[3] [https://github.com/JdeRobot/DL-Studio/pull/5](https://github.com/JdeRobot/DL-Studio/pull/5)
{: .text-justify}

### Pull Requests Closed

[1] [https://github.com/JdeRobot/BehaviorMetrics/pull/182](https://github.com/JdeRobot/BehaviorMetrics/pull/182) \\
[2] [https://github.com/JdeRobot/BehaviorMetrics/pull/183](https://github.com/JdeRobot/BehaviorMetrics/pull/183) \\
[3] [https://github.com/JdeRobot/BehaviorMetrics/pull/184](https://github.com/JdeRobot/BehaviorMetrics/pull/184) \\
[4] [https://github.com/JdeRobot/BehaviorMetrics/pull/185](https://github.com/JdeRobot/BehaviorMetrics/pull/185)
{: .text-justify}