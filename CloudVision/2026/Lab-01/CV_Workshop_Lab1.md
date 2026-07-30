# CloudVision Lab 01 
## Inventory and Topology 
![CloudVision](images/cv-logo.png)

## This Lab Guide:



[CloudVision Workshop Lab Guide 01- Inventory and Topology ](https://github.com/arista-rockies/Workshops/blob/main/CloudVision/2026/Lab-01/CV_Workshop_Lab1.md)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Accessing The Lab](#2-accessing-lab)

---

# 1. Lab Topology

![Full Lab Topology](images/a-topology.png)

---
# 2. Accessing The Lab

VERY ELABORATE LOGIN SECTION TO FOLLOW - Need to verify how we are doing this first. Here is a picture of a dog as a placeholder.

![Login](images/login-1.png)

---
# 3. Lab Details
## Lab Overview
In this lab we will onboard devices to the **Inventory and Topology Studio**. This is the first action required to allow devices to be configured using the CloudVision Studios.

## Inputs
The following is all of the information that you will need complete this lab. Feel free to name your devices as you see fit. Understand the hostnames will be used to identify devices in later labs.


|**DeviceID**| **HOSTNAME** |
| :----------: | :------------: |
| CampusA-Spine1 |	P[$POD#]-CampusA-Spine1 |
| CampusA-Spine2 |	P[$POD#]-CampusA-Spine2 |
| CampusA-Leaf1a |	P[$POD#]-CampusA-Leaf1A |
| CampusA-Leaf1b |	P[$POD#]-CampusA-Leaf1B |
| CampusA-Leaf1-1|	P[$POD#]-CampusA-Leaf1-1 |
| CampusA-Leaf2 |	P[$POD#]-CampusA-Leaf2 |
| CampusA-Host1 |	P[$POD#]-CampusA-Host1 |


## Lab Steps:
1. Using the blue navigation pane on the left: Navigate to **Provisioning** > **Studios**

![Studio Navigation](images/studio-nav.png)

2. Under the Essential Studios section locate and select the **Inventory and Topology** Studio

![Studio Inventory and Topology](images/iandt-studio.png)

3. Notice that there are currently no Registered Devices listed. We need to register our devices to this studio before we can begin making configuration changes. Locate the devices that are in ZTP by selecting **Network Updates**

![I&T Network Updates](images/iandt-updates.png)

4. Select all of the ZTP'd devices with an **Update** status of **Device Added**. Select all device and select **Accept Updates**

![I&T Network Updates](images/iandt-accept.png)

5. Return to the the **Registered Devices** tab

![I&T Network Registered Devices](images/iandt-reg-dev.png)

6. The lab devices that are currently in ZTP will now be shown under the registered devices. In the **Hostname** field for each device add the intended hostnaem for the device.

[!NOTE]
We will be utilizing Universal Cloud Network Architecture to identify devices type in future lab guides (Leaf, Spine, Member Leaf, Border Leaf), so try and make it easy for yourself to identify those device types in your naming convention.

![I&T Hostnames](images/iandt-hostnames.png)

7. After you have updated the **Hostname** value for each device, we now need to save these changes to CloudVision. Select the **Clipboard** icon in the Workspace Island toolbar in the bottom center of your screen.

![Workspace Island Review](images/iandt-hostnames.png)


8. After the workspace builds, there should be no device configuration changes within the lab. However, we have added the devices to the Inventory and Topology Studio. We will **Submit Workspace** to save those changes.

![Submit Workspace](images/iandt-submit.png)

![Exit Workspace](images/exit-workspace.png)
---


**LAB GUIDE COMPLETE**
