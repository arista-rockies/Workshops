# CloudVision Lab 04
## Onboarding a network using Network Hierarchy 
![CloudVision](images/cv-logo.png)

## This Lab Guide:

[CloudVision Workshop Lab Guide 01 - Inventory and Topology](https://github.com/arista-rockies/Workshops/blob/jdarrish-labs/CloudVision/2026/Lab-04/CV_Workshop_Lab4.md)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Accessing the Lab](#2-accessing-the-lab)
3. [Lab Details](#3-lab-details)

---

# 1. Lab Topology

![Full Lab Topology](images/a-topology.png)

---

# 2. Accessing the Lab

To authenticate to CloudVision you will need to visit the following page:

[CloudVision Auth](https://labs.arista.com/ignition/event/9gk8a4d3)

Each attendee will be provided with a unique access key. Enter you access key and select the Blue Arrow


![Ignition Login](images/ignition-login.png)

After successfully authenticated you will should see **CVaaS** available under Services. Selecting the CVaaS tile will authenticate you directly to the Lab CVaaS environment

![Ignition Login](images/cvaas-tile.png)

![CVaaS Home](images/cvaas-access.png)

---

# 3. Lab Details

## Lab Overview

In this lab, we will onboard devices using CloudVisions **Network Hierarchy**. This step optimizes the process of deploying a new network using CloudVision.

## Inputs

The following is all of the information you will need to complete this lab. Feel free to name your devices as you see fit. Keep in mind that the hostnames will be used to identify devices in later labs.

| **HOSTNAME** | **DEVICE ID** |
| :----------: | :------------: |
| CampusB-Spine1 | P[$POD#]-CampusB-Spine1 |
| CampusB-Spine2 | P[$POD#]-CampusB-Spine2 |
| CampusB-Leaf1a | P[$POD#]-CampusB-Leaf1A |
| CampusB-Leaf1b | P[$POD#]-CampusB-Leaf1B |
| CampusB-Leaf1c | P[$POD#]-CampusB-Leaf1C |
| CampusB-Leaf2a | P[$POD#]-CampusB-Leaf2A |

## Lab Steps:

1. Let's confirm which devices are those we will include in the CampusB deployment. Using the blue navigation pane on the left, navigate to **Devices** > **Inventory**.
2. In the list of devices reporting in to your CloudVision instance, notice those whose hostname has an IP address in it. Look to the right at the **DeviceID** column. There you will see the **DeviceID** of those we will use in the **CampusB** fabric.

![Studio Navigation](images/studio-nav.png)

3. Now, let's proceed to the Network Hierarchy by using the blue navigation pane on the left, and selecting the **Network Hierarchy** option in the list. It should be the 3rd icon down below the cloud.

![Studio Inventory and Topology](images/iandt-studio.png)

4. Next, hover over the **Workshop** Campus in the menu on the left. Three dots should appear to the right. Select those dots and click **Add Campus Pod**. Name it **CampusB** 

> [!NOTE]
> We will be utilizing Universal Cloud Network Architecture to identify device types in future lab guides (Leaf, Spine, Member Leaf, Border Leaf), so try to make it easy for yourself to identify those device types in your naming convention.

![I&T Hostnames](images/iandt-hostnames.png)

5. For **Topology Type**, select: **L2 - L2 Leaf Spine**

![I&T Hostnames](images/iandt-hostnames.png)
   
6. On **Protocols**: Do nothing
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

7. On **IP Addressing**:
	1. 172.31.0.0/24
	2. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

8. On **In-Band Management**: 
	1. Disable it using the "Enable in-band management and configure its default settings" Toggle
	2. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

9. On **Out-of-Band Management**: 
	1. Enable it using the "Enable out-of-band management and configure its default settings" Toggle
	2. Create a Profile - Include OOB in the name
		1. Management VRF Name: MGMT
		2. IP Address Allocation Method: DHCP
	3. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

10. On **Source Interface**:
	1. Spine Source Interface:
		1. Source Type: **Out-of-band**
		2. Source VRF: **MGMT**
	2. Leaf Source Interface:
		1. **Same**
	3. Member-Leaf Source Interface
		1. **Same**
	4. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

11. On **Spanning Tree**:
	1. **Spine Spanning Tree**: 
		1. Mode: **Rapid-PVST**
		2. Priority: **4096**
	2. **Access-Pod Spanning Tree**
		1. Mode: **Rapid-PVST**
		2. Priority: **32768**
	3. **Member Leaf Spanning Tree Priority**
		1. Priority: **61440**
	4. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

12. On **MLAG**:
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

13. On **802.1X**:
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

14. On **Multicast**:
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

15. On **IP Locking**:
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)
    
16. On **PTP**:
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

17. On **VLANs**
	1. **Create VLAN 10, 20, 30**
		1. Name them whatever you want
		2. **VLAN Type: "L2 Only"**
		3. Don't worry about any of the other fields or features
	2. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

18. On **Static Configuration**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

19. On **Next Steps for this Campus Pod**
	1. Click Continue under "Add Spines Devices"

![I&T Hostnames](images/iandt-hostnames.png)

20. On **Device Assignment**
	1. In the dashed box, click **"+ Add Device"**
	2. Find and select both of the Spine switches for CampusB
		1. Click Confirm Selection
		2. Give each a name:
			1. Spine1
			2. Spine2
			3. Leave the Role as "Spine"
	3. Click **Add Devices**
	4. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

21. On **Software Version**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

22. On **Protocols**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

23. On **External Devices**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

24. On **Static Routes**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

25. On **Transit SVIs**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

26. On **Static Configuration**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

27. On **Next Steps**
	1. Under **"Add and Configure an Access Pod"**
		1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

		3. Name this Access-Pod:Pod1
	2. Click Add Access Pod

![I&T Hostnames](images/iandt-hostnames.png)
  
28. On **Device Assignment**
	1. In the dashed box, click **"+ Add Device"**
	2. Find and select **Leaf1A, Leaf1B & Leaf1C** switches
		1. Click Confirm Selection
		2. **Give each a name:**
			1. Leaf1A
				1. Select Role: **Leaf**
			2. Leaf1B
				1. Select Role: **Leaf**
			3. Leaf1C
				1.  Select Role: **Member-Leaf**

![I&T Hostnames](images/iandt-hostnames.png)

	2. **Click Add Devices**
		1. Confirm the Hostnames look correct
			1. If they didn't take, select the pencil to the right of each of them and rename them accordingly 
	3. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)
  
29. On **MLAG Pairs**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

30. On **Software Version**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

31. On **VLANs**
	1. **In the dashed box, click "+ Add VLAN"**
		1. Add all three VLANs to this Access Pod
	2. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

32. On **External Devices**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

33. On **Static Routes**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

34. On **Transit SVIs**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

35. On **Static Configuration**
	1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

36. On Next Steps (Next Steps for this Access Pod)
  1. **Don't click "Click Review and Submit".**
  2. Instead, **we need to add the 2nd Access Pod**
  3. Next, hover over the **CampusB) Campus in the menu on the left. Three dots should appear to the right. Select those dots and click **Add Access Pod**.
    1. Name this Access-Pod: Pod2
  5. Click **Add Access Pod**

![I&T Hostnames](images/iandt-hostnames.png)

37. On **Device Assignment**
  1. In the dashed box, click **"+ Add Device"**
  2. Find and select Leaf2A switch
  3. Click Confirm Selection
  4. Give the switch a name:
    1. **Leaf2A**
      1. Select Role: **Leaf**
  5. Click **Add Devices**
    1. Confirm the Hostname look correct
      1. If they didn't take, select the pencil to the right of each of them and rename them accordingly
  6. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

38. On **Software Version**
  1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

39. On **VLANs**
  1. In the dashed box, click "+ Add VLAN"
    1. **Add all three VLANs to this Access Pod**
  2. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

40. On **External Devices**
  1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

41. On **Static Routes**
  1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

42. On **Transit SVIs**
  1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

43. On **Static Configuration**
  1. Click Continue

![I&T Hostnames](images/iandt-hostnames.png)

44. On Next Steps (Next Steps for this Access Pod)
  1. Now click **"Review and Submit"**.

![I&T Hostnames](images/iandt-hostnames.png)

45. You will be presented with the Workspace Review page, with a summation of all of the things you have done.
  1. **Review the Proposed Configuration Changes below**
    1. Text with a Green Highlight = Configuration that will be added
    2. Text with a Blue Highlight = Configuration that will be modified
    3. Text with a Red Highlight = Configuration that will be removed

![I&T Hostnames](images/iandt-hostnames.png)
     
      1. Question: Why is there so much Red Highlighted text?
        1. Answer: This is because, as we proceed to put these switches into production, we are taking them out of ZTP mode and therefore removing many of the no-longer needed Factory Default configuration settings. 
    4. After reviewing the proposed changes, scroll up in the Workspace window
      1. At the top right, select **Submit Workspace**
46. Click View Change Control

![I&T Hostnames](images/iandt-hostnames.png)

47. **You will be taken to the respective Change Control**, where your changes will be enacted
  1. Then **click Review and Approve at the top right**

![I&T Hostnames](images/iandt-hostnames.png)

48. **Review the details of your Change Control one last time**
49. **Click Approve and Execute at the bottom right** to tell CloudVision to push the configuration to the devices
  1. The Change Control has now been activated

![I&T Hostnames](images/iandt-hostnames.png)

50. **Click the Logs button at the far right** of the Change Control screen to view live messages being exchanged between CloudVision and the Switches

![I&T Hostnames](images/iandt-hostnames.png)

51. **The Fabric deployment & Change Control will take between 15-20 minutes to complete**
 
---

**LAB GUIDE COMPLETE**
