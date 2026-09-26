# CloudVision Lab 04
## Onboarding a network using Network Hierarchy 
![CloudVision](images/cv-logo.png)

## This Lab Guide:

[CloudVision Workshop Lab Guide 04 - Network Hierarchy Provisioning](https://github.com/arista-rockies/Workshops/blob/main/CloudVision/2026/Lab-04/README.md)

---

## Table of Contents
1. [Lab Topology](#1-lab-topology)
2. [Accessing the Lab](#2-accessing-the-lab)
3. [Lab Details](#3-lab-details)

---

# 1. Lab Topology

![Full Lab Topology](images/lab-topology.png)

---

# 2. Accessing the Lab

To authenticate to CloudVision, you will need to visit the following page. Please select the correct event you are currently in:


[**UVU: October 1st-2nd**](https://labs.arista.com/ignition/event/g7nwnc9c)

[**UofU: October 8th-9th**](https://labs.arista.com/ignition/event/ehnenmpn)

[**Idaho: October 14th-15th**](https://labs.arista.com/ignition/event/kpd99dy8)

[**Colorado: Oct 21st-22nd**](https://labs.arista.com/ignition/event/kxpd9ttr)


Each attendee will be provided with a unique access key. Enter your access key and select the Blue Arrow

![Ignition Login](images/ignition-login.png)


After successfully authenticating, you should see **CVaaS** available under Services. Selecting the CVaaS tile will authenticate you directly to the Lab CVaaS environment

![Ignition Login](images/cvaas-tile.png)

![CVaaS Home](images/cvaas-access.png)

---

# 3. Lab Details

## Lab Overview

In this lab, we will onboard devices using CloudVision's **Network Hierarchy**. This step optimizes the process of deploying or updating a new or existing network.

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

![Studio Navigation](images/image1.png)

3. Now, let's proceed to the Network Hierarchy by using the vertical blue navigation pane on the left, and selecting the **Network Hierarchy** option in the list. It should be the 3rd icon down below the cloud.

![Studio Inventory and Topology](images/image2.png)

4. On the left side, click on the existing Campus: **Workshop**. Let's modify some Campus-wide configuration elements.

> [!NOTE]
> We will be utilizing Universal Cloud Network Architecture to identify device types in future lab guides (Leaf, Spine, Member Leaf, Border Leaf), so try to make it easy for yourself to identify those device types in your naming convention.

5. Select the **Configuration** tab

![I&T Hostnames](images/image3.png)
   
6. On **DNS**
	1. Create a **DNS Profile** by
		1. Click in the Profile field
		2. Type a name for your profile: **DNS-Servers**
			1.  After you've typed the name, click the **"+Create DNS-Servers"** option below or it will not create the profile
		3. Options will appear below. Click the **"+ Add Server"** option
			1. In the **"Server IP Address"** field, enter: **1.1.1.1**
			2. Leave the Priority as **Default**
			3. Click **Add**
			4. Add another DNS server: **8.8.8.8**
		4. Click **Save** at the top right

![I&T Hostnames](images/image3.png)
![I&T Hostnames](images/image5.png)
![I&T Hostnames](images/image4.png)

7. Skip past **NTP**

8. On **Local Users** (left side):
	1. Select **"+Add User"**
		1. Name: **superuser**
		2. Create a **"Assigned User Groups"**
			1. Name: **ug-superuser**
			2. Once you've typed the name, **ensure you click the "+ Create ug-superuser" sign below or it won't actually create the User Group**
			3. Role: **network-admin**
			4. Privilege: **15**
			5. Password Type: **Plain Text**
			6. Password: **aristarocks!**
		3. Click **Add**
	2. Select the dropdown menu under **"User Group"**
		1. **Select the User Group (ug-superuser)** you just created in the drop-down menu
	3. Click **Save**

![I&T Hostnames](images/image7.png)
![I&T Hostnames](images/image8.png)

9. Skip past **AAA**

10. On Streaming Agent
	1. Click the **"+ Configure"** option below 
	2. Select **Disabled**
	3. Click **Save**

![I&T Hostnames](images/image9.png)

11. On **VRFs**
	1. Click the **"+ Configure"** option below 
		1. Name: **MGMT**
	2. Click **Create**
	3. Click **Save**

![I&T Hostnames](images/image10.png)
![I&T Hostnames](images/image11.png)
![I&T Hostnames](images/image12.png)

12. Skip **Static Configuration**

13. Now, let's deploy a new **Campus-Pod** under **Workshop**
	1. Next, **hover over the Campus named Workshop** in the Network Hierarchy menu on the left. **Three dots should appear** to the right. Select those dots and click **Add Campus Pod**.
		1. Call it: **CampusB**

![I&T Hostnames](images/image14.png)

14. For **Topology Type**, select: **L2 - L2 Leaf Spine**
	1. Click **Continue**

![I&T Hostnames](images/image15.png)

15. On **Protocols**: Do nothing
	1. Click **Continue**

![I&T Hostnames](images/image16.png)
    
16. On **IP Addressing**: 
	1. Enter **172.31.0.0/24**
	2. Click **Continue**

![I&T Hostnames](images/image17.png)

17. On **In-Band Management**: 
	1. **Disable** it using the "Enable in-band management and configure its default settings" Toggle
	2. Click **Continue**

![I&T Hostnames](images/image18.png)

18. On **Out-of-Band Management**: 
	1. **Enable** it using the "Enable out-of-band management and configure its default settings" Toggle
	2. Create a **Profile**
		1. Name: **CampusB_OOB**
		2. Management VRF Name: **MGMT**
		3. IP Address Allocation Method: **DHCP**
	3. Click **Continue**

![I&T Hostnames](images/image19.png)
![I&T Hostnames](images/image20.png)

19. On **Source Interface**:
	1. **Spine Source Interface**:
		1. Source Type: **Out-of-band**
		2. Source VRF: **MGMT**
	2. Leaf Source Interface:
		1. **Same**
	3. Member-Leaf Source Interface
		1. **Same**
	4. Click **Continue**

![I&T Hostnames](images/image21.png)

20. On **Spanning Tree**:
	1. **Spine** Spanning Tree: 
		1. Mode: **Rapid-PVST**
		2. Priority: **4096**
	2. **Access-Pod** Spanning Tree
		1. Mode: **Rapid-PVST**
		2. Priority: **32768**
	3. **Member Leaf** Spanning Tree Priority
		1. Priority: **61440**
	4. Click **Continue**

![I&T Hostnames](images/image22.png)

21. 9. On **MLAG**:
	1. Click **Continue**

![I&T Hostnames](images/image23.png)

22. 10. On **802.1X:**
	1. Click **Continue**

![I&T Hostnames](images/image24.png)

23. 11. On **Multicast**:
	1. Click **Continue**

![I&T Hostnames](images/image25.png)

24. 12. On **IP Locking**:
	1. Click **Continue**

![I&T Hostnames](images/image26.png)

25. 13. On **PTP**:
	1. Click **Continue**

![I&T Hostnames](images/image27.png)

26. On **VLANs**
	1. Create **VLAN 10, 20, 30**
		1. Name: **Whatever you want**
		2. VLAN Type: "**L2 Only**"
		3. **Ignore other fields** or features
		4. Click **Save and Repeat**
	2. Click **Continue**

![I&T Hostnames](images/image28.png)
![I&T Hostnames](images/image29.png)
![I&T Hostnames](images/image30.png)

27. On **Static Configuration**
	1. Click **Continue**

![I&T Hostnames](images/image31.png)

28. On **"Next Steps for this Campus Pod"**
	1. Click **Continue** under **"Add Spines Devices"**

![I&T Hostnames](images/image32.png)
  
29. On **Device Assignment**
	1. In the dashed box, click **"+ Add Device"**
	2. **Find and select** both of the **Spine switches** for **CampusB**
		1. Click **Confirm Selection**
		2. Give each a **name**:
			1. **CampusB-Spine1**
			2. **CampusB-Spine2**
			3. Leave the **Role as "Spine"**
	3. Click **Add Devices**
	4. Click **Continue**

![I&T Hostnames](images/image33.png)
![I&T Hostnames](images/image34.png)

30. On **Software Version**
	1. Click **Continue**

![I&T Hostnames](images/image35.png)
  
31. On **Protocols**
	1. Click **Continue**

![I&T Hostnames](images/image36.png)

32. On **External Devices**
	1. Click **Continue**

![I&T Hostnames](images/image7.png)

33. On **Static Routes**
	1. Click **Continue**

![I&T Hostnames](images/image38.png)

34. On **Transit SVIs**
	1. Click **Continue**

![I&T Hostnames](images/image39.png)

35. On **Static Configuration**
	1. Click **Continue**

![I&T Hostnames](images/image40.png)

36. On **Next Steps**
	1. Under **"Add and Configure an Access Pod"** to the right
		1. Click **Continue**
		2. Name this Access-Pod: **Pod1**
	2. Click **Add Access Pod**

![I&T Hostnames](images/image41.png)
![I&T Hostnames](images/image42.1.png)

37. On **Device Assignment**
	1. In the dashed box, click **"+ Add Device"**
	2. **Find and select Leaf1A, Leaf1B & Leaf1C switches**
		1. Click **Confirm Selection**
		2. Give each a name:
			1. **CampusB-Leaf1A**
				1. Select Role: **Leaf**
			2. **CampusB-Leaf1B**
				1. Select Role: **Leaf**
			3. **CampusB-Leaf1C**
				1.  Select Role: **Member-Leaf**
	3. **Click Add Devices**
		1. Confirm the Hostnames look correct
			1. If they didn't take, select the pencil to the right of each of them and rename them accordingly 
	4. Click **Continue**

![I&T Hostnames](images/image41.1.png)
![I&T Hostnames](images/image42.png)

38. On **MLAG Pairs**
	1. Click **Continue**

![I&T Hostnames](images/image43.png)

39. On **Software Version**
	1. Click **Continue**

![I&T Hostnames](images/image44.png)

40. On **VLANs**
	1. In the dashed box, click **"+ Add VLAN"**
		1. **Add all three VLANs** you created earlier to this Access Pod
	2. Click **Continue**

![I&T Hostnames](images/image45.png)

41. On **External Devices**
	1. Click **Continue**

![I&T Hostnames](images/image46.png)

42. On **Static Routes**
	1. Click **Continue**

![I&T Hostnames](images/image47.png)

43. On **Transit SVIs**
	1. Click **Continue**

![I&T Hostnames](images/image48.png)

44. On **Static Configuration**
	1. Click **Continue**

![I&T Hostnames](images/image49.png)

45. On Next Steps (**Next Steps for this Access Pod**)
	1. **Don't** click  "Review and Submit"
		1. If you do though, no worries. Just hit the X at the top right of the Workspace window and you'll be right back were you were.
		2. Instead, **we need to add the 2nd Access Pod**
	2. Next, **hover over the CampusB Campus** in the menu on the left. Three dots should appear to the right. Select those dots and click **Add Access Pod**.
		1. Name this Access-Pod: **Pod2**
	3. Click **Add Access Pod**

![I&T Hostnames](images/image50.png)
![I&T Hostnames](images/image51.png)
![I&T Hostnames](images/image52.png)

46. On **Device Assignment**
	1. In the dashed box, click **"+ Add Device"**
	2. Find and select **Leaf2A** switch
	3. Click **Confirm Selection**
	4. Give the switch a name:
		1. **CampusB-Leaf2A**
			1. Select Role: **Leaf**
	5. Click **Add Devices**
		1. Confirm the Hostname look correct
			1. If they didn't take, select the pencil to the right of each of them and rename them accordingly 
	6. Click **Continue**

![I&T Hostnames](images/image53.png)

47. On **Software Version**
	1. Click **Continue**

![I&T Hostnames](images/image54.png)
     
48. On **VLANs**
	1. In the dashed box, click **"+ Add VLAN"**
		1. **Add all three VLANs to this Access Pod**
	2. Click **Continue**

![I&T Hostnames](images/image55.png)

49. On **External Devices**
	1. Click **Continue**

![I&T Hostnames](images/image56.png)

50. On **Static Routes**
	1. Click **Continue**

![I&T Hostnames](images/image57.png)

51. On **Transit SVIs**
	1. Click **Continue**

![I&T Hostnames](images/image58.png)

52. On **Static Configuration**
	1. Click **Continue**

![I&T Hostnames](images/image59.png)

53. On **Next Steps (Next Steps for this Access Pod)**
	1. **Now click "Review and Submit"**.

![I&T Hostnames](images/image60.png)

54. You will be presented with the **Workspace Review page**, with a summation of all of the things you have done.
	1. Review the **Proposed Configuration** Changes below
		1. Text with a **Green Highlight** = Configuration that will be **added**
		2. Text with a **Blue Highlight** = Configuration that will be **modified**
		3. Text with a **Red Highlight** = Configuration that will be **removed**
			1. Question: Why is there so much Red Highlighted text?
				1. Answer: This is because, as we proceed to put these switches into production, we are taking them out of ZTP mode and therefore removing many of the no-longer needed Factory Default configuration settings. 
		4. After reviewing the proposed changes, **scroll up in the Workspace window**
			1. At the top right, select **Submit Workspace**

![I&T Hostnames](images/image61.png)
![I&T Hostnames](images/image62.png)

55. Click **View Change Control**

56. **You will be taken to the Change Control, where your changes will be deployed**
	1. There will be changes to both the CampusA and CampusB network. This is expected.
	2. Then click **Review and Approve** at the top right
	3. Review the details of your Change Control one last time
	4. Turn on the t**oggle at the bottom right "Execute immediately"** and **click Approve and Execute** at the bottom right to tell CloudVision to push the configuration to the devices
	5. The **Change Control has now been activated**

![I&T Hostnames](images/image63.png)
![I&T Hostnames](images/image64.png)
![I&T Hostnames](images/image65.png)

57. Click the **Logs button** at the far right of the Change Control screen to view live messages being exchanged between CloudVision and the Switches

![I&T Hostnames](images/image66.png)
![I&T Hostnames](images/image67.png)

58. The Change Control will take between 10-15 minutes to complete

---

**LAB GUIDE COMPLETE**
